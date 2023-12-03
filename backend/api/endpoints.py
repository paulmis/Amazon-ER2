from sqlalchemy import func
from flask import jsonify, request, redirect, make_response, Response
from sqlalchemy.sql import False_
from sqlalchemy.sql.operators import or_
from flask import jsonify, request
from . import app, db
import base64
from .models import Comment, LLM_Result
from sqlalchemy.orm import load_only, defer
from .analyzer import *
from .ai.interface import analyze_comments, cluster_llm_results, generate_image, get_highlight
import time
import os

ROWS_PER_PAGE = 100

row_to_json = lambda row: {
    column: getattr(row, column) for column in row.__table__.c.keys()
}


def _make_llm_behave(l):
    llm_result = row_to_json(l)
    for j in llm_result["issues"]:
        if "embedding" in j:
            j.pop("embedding")

    return llm_result


def _merge_comment_and_llm(t):
    comment = row_to_json(t[0])
    if t[1]:
        comment["llm_result"] = _make_llm_behave(t[1])

    return comment


def _get_issue_severities_from_comment_ids(comment_ids):
    filter = False_()
    for i in comment_ids:
        filter = or_(i == LLM_Result.comment_id, filter)

    res = LLM_Result.query.filter(filter).all()
    severities = {"high": 0, "medium": 0, "low": 0}
    for i in res:
        for j in i.issues:
            s = j["severity"]
            severities[s] = severities.get(s, 0) + 1

    return severities


@app.route("/query", methods=["GET"])
def get_products():
    page = request.args.get("page", 1, type=int)
    count = request.args.get("count", ROWS_PER_PAGE, type=int)

    search_dict = request.args.copy()

    if "page" in search_dict:
        search_dict.pop("page")

    if "count" in search_dict:
        search_dict.pop("count")

    products = Comment.query.filter_by(**search_dict).paginate(
        page=page, per_page=count
    )

    return jsonify({"products": list(map(_merge_comment_and_llm, products))})


def _aggregate_unique_helper(field, value, page, count, query):
    vals = (
        Comment.query.with_entities(field, func.count(field))
        .filter_by(**query)
        .filter(field.ilike(value))
        .outerjoin(LLM_Result)
        .group_by(field)
        .order_by(func.sum(LLM_Result.issue_count).desc())
        .paginate(page=page, per_page=count)
    )
    unique_vals = [{"value": x[0], "total_count": x[1]} for x in vals]

    llm_vals = (
        Comment.query.with_entities(field, func.count(field))
        .join(LLM_Result)
        .group_by(field)
        .all()
    )

    llm_counts = {x[0]: x[1] for x in llm_vals}

    for i in unique_vals:
        lc = llm_counts.get(i["value"], 0)

        if (
            lc > 0
        ):  # Aggregate issue severities if they have aready been put through the LLM
            vals = (
                Comment.query.with_entities(Comment.id)
                .filter(field.__eq__(i["value"]))
                .all()
            )
            ids = list(map(lambda x: x[0], vals))
            i["severities"] = _get_issue_severities_from_comment_ids(ids)

        i["llm_result_count"] = llm_counts.get(i["value"], 0)

    return unique_vals


@app.route("/aggregate_unique", methods=["GET"])
def aggregate_unique():
    page = request.args.get("page", 1, type=int)
    count = request.args.get("count", ROWS_PER_PAGE, type=int)

    field = request.args.get("field", None)
    search_value = "%" + request.args.get("query", "") + "%"

    query = {x[0] : x[1] for x in request.args.items() if x[0] not in ['page', 'count', 'field', 'query']}
    if field == "product":
        vals = _aggregate_unique_helper(Comment.product, search_value, page, count, query)
    elif field == "brand":
        vals = _aggregate_unique_helper(Comment.brand, search_value, page, count, query)
    else:
        return jsonify([])

    return jsonify(vals)


def _get_comment_with_id(search_result, id):
    for i in search_result:
        if i[0].id == id:
            return i[0]
    return None


def aggregate_issues_by_query(query_dicts, granularity=1):
    res = []
    for query_dict in query_dicts:
        res += (
            db.session.query(Comment, LLM_Result)
            .filter_by(**query_dict)
            .outerjoin(LLM_Result)
            .all()
        )

    comments_missing_llm_results = list(
        map(lambda x: x[0], filter(lambda x: x[1] is None, res))
    )
    bedrock_results = analyze_comments(comments_missing_llm_results)

    db.session.add_all(bedrock_results)
    db.session.commit()

    llm_res_map = {}
    for i in range(len(comments_missing_llm_results)):
        llm_res_map[comments_missing_llm_results[i].id] = bedrock_results[i]

    combined = []
    for i in res:
        if i[0]:
            d = row_to_json(i[0])
            if d["id"] in llm_res_map:
                i[0].llm_result = llm_res_map[d["id"]]
                i = (i[0], llm_res_map[d["id"]])
        else:
            continue
        if i[1]:
            d2 = row_to_json(i[1])
            d2.pop("id")
            d.update(d2)
        if d:
            combined.append(d)

    llm_results = list(filter(lambda x: x, map(lambda x: x[0].llm_result, res)))
    clusters = cluster_llm_results(llm_results)

    final_result = []
    for i in clusters:
        tmp = {
            "name": i,
            "item_count": len(set([x[0] for x in clusters[i]])),
            "issues": [_make_llm_behave(x[0])["issues"][x[1]] for x in clusters[i]],
        }

        severities = {"high": 0, "medium": 0, "low": 0}
        for j in clusters[i]:
            if foo := _get_comment_with_id(res, j[0].comment_id):
                tmp["example"] = row_to_json(foo)
            s = j[0].issues[j[1]]["severity"]
            severities[s] = severities.get(s, 0) + 1
        tmp["severities"] = severities
        final_result.append(tmp)

    return final_result


def get_all_reviews_in_cluster(query_dicts, cluster_name, granularity=1):
    res = []
    for query_dict in query_dicts:
        res += (
            db.session.query(Comment, LLM_Result)
            .filter_by(**query_dict)
            .join(LLM_Result)
            .all()
        )

    llm_results = list(filter(lambda x: x, map(lambda x: x[0].llm_result, res)))
    clusters = cluster_llm_results(llm_results)

    if cluster_name not in clusters:
        return []

    reviews = {}

    for i in clusters[cluster_name]:
        comment = row_to_json(_get_comment_with_id(res, i[0].comment_id))
        llm_result = row_to_json(i[0])

        for j in llm_result["issues"]:
            if "embedding" in j:
                j.pop("embedding")

        comment["llm_result"] = llm_result
        reviews[comment["id"]] = comment

    return list(reviews.values())


@app.route("/issues", methods=["GET"])
def get_issues():
    queries = []
    for i in request.args:
        for j in request.args.getlist(i):
            queries.append({i: j})

    results = aggregate_issues_by_query(queries)

    return jsonify(results)


@app.route("/issues_for_cluster", methods=["GET"])
def get_reviews_in_cluster():
    queries = []
    cluster_name = None
    print(request.args)
    for i in request.args:
        if i == "cluster_name":
            cluster_name = request.args[i]
            continue
        for j in request.args.getlist(i):
            queries.append({i: j})

    if not cluster_name:
        return []

    results = get_all_reviews_in_cluster(queries, cluster_name)
    return jsonify(results)


@app.route("/image", methods=["GET"])
def get_image():
    product_name = request.args.get("product")
    if not product_name:
        return jsonify({"error": "No product name provided"}), 400

    base64_image = generate_image(
        product_name
    )  # This should return the base64 image string

    # Decode the base64 string
    image_binary = base64.b64decode(base64_image)

    # Return the binary data with the correct content type
    return Response(
        image_binary, mimetype="image/png"
    )  # Or 'image/jpeg' depending on your image format

@app.route("/highlight", methods=["POST"])
def highlight():
    # Gets a product review text and a issue name and returns a segment of the text
    
    product_review = request.json.get("product_review")
    issue = request.json.get("issue")
    if not product_review:
        return jsonify({"error": "No product review provided"}), 400
    if not issue:
        return jsonify({"error": "No issue provided"}), 400
    
    highlight = get_highlight(product_review, issue)
    return jsonify({"highlight": highlight})
