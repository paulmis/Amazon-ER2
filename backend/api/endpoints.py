from flask import jsonify, request
from . import app, db
from .models import Comment, LLM_Result
from sqlalchemy.orm import load_only, defer
from .analyzer import *
from .ai.interface import analyze_comments, cluster_llm_results
import time

ROWS_PER_PAGE = 100

row_to_json = lambda row: {column: getattr(row, column) for column in row.__table__.c.keys()}

@app.route('/query', methods=['GET'])
def get_products():
    page = request.args.get('page', 1, type=int)
    count = request.args.get('count', ROWS_PER_PAGE, type=int)

    search_dict = request.args.copy()

    if 'page' in search_dict:
        search_dict.pop('page')

    if 'count' in search_dict:
        search_dict.pop('count')

    products = Comment.query.filter_by(**search_dict).paginate(page=page, per_page=count)

    return jsonify({'products': list(map(row_to_json, products))})

@app.route('/aggregate_unique', methods=['GET'])
def aggregate_unique():
    page = request.args.get('page', 1, type=int)
    count = request.args.get('count', ROWS_PER_PAGE, type=int)

    field = request.args.get('field', None)
    if field == 'product':
        vals = Comment.query.group_by(Comment.product).paginate(page=page, per_page=count)
        unique_vals = [val.product for val in vals]

        return jsonify({'values': unique_vals})
    elif field == 'brand':
        vals = Comment.query.group_by(Comment.brand).outerjoin(Comment.llm_result).paginate(page=page, per_page=count)

        unique_vals = [val.brand for val in vals]

        return jsonify({'values': unique_vals})
    else:
        return jsonify({})

def _get_comment_with_id(search_result, id):
    for i in search_result:
        if i[0].id == id:
            return i[0]
    return None

def aggregate_issues_by_query(query_dicts, granularity=1):
    res = []
    for query_dict in query_dicts:
        res += db.session.query(Comment, LLM_Result).filter_by(**query_dict).outerjoin(LLM_Result).all()

    comments_missing_llm_results = list(map(lambda x: x[0], filter(lambda x: x[1] is None, res)))
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
            if d['id'] in llm_res_map:
                i[0].llm_result = llm_res_map[d['id']]
                i = (i[0], llm_res_map[d['id']])
        else:
            continue
        if i[1]:
            d2 = row_to_json(i[1])
            d2.pop('id')
            d.update(d2)
        if d:
            combined.append(d)

    llm_results = list(filter(lambda x: x, map(lambda x: x[0].llm_result, res)))
    clusters = cluster_llm_results(llm_results)

    final_result = {}
    for i in clusters:
        final_result[i] = {
            "item_count": len(clusters[i])
        }

        for j in clusters[i]:
            if (foo := _get_comment_with_id(res, j[0].comment_id)):
                final_result[i]["example"] = row_to_json(foo)
                

    return final_result

@app.route('/issues', methods=['GET'])
def get_issues():
    queries = []
    for i in request.args:
        for j in request.args.getlist(i):
            queries.append({i:j})

    results = aggregate_issues_by_query(queries)

    return jsonify(results)
