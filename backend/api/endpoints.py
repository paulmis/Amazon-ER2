from flask import jsonify, request
from . import app, db
from .models import Comment, LLM_Result
from sqlalchemy.orm import load_only, defer
from .analyzer import *
from .ai import interface

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

def aggregate_issues_by_query(query_dict, granularity=1):
    res = db.session.query(Comment, LLM_Result).filter_by(**query_dict).outerjoin(LLM_Result).all()

    combined = []
    for i in res:
        if i[0]:
            d = row_to_json(i[0])
        else:
            continue
        if i[1]:
            d2 = row_to_json(i[1])
            d2.pop('id')
            d.update(d2)
        else:
            # Make a call to bedrock LLM here
            pass
        if d:
            combined.append(d)

    # Cluster here

    return combined

@app.route('/issues', methods=['GET'])
def get_issues():
    results = []
    for i in request.args:
        for j in request.args.getlist(i):
            results.append(aggregate_issues_by_query({i: j}))

    return jsonify(results)
