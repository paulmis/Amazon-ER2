from flask import jsonify, request
from . import app
from .models import Product
from sqlalchemy.orm import load_only, defer

ROWS_PER_PAGE = 100

row_to_json = lambda row: {column: str(getattr(row, column)) for column in row.__table__.c.keys()}

@app.route('/query', methods=['GET'])
def get_products():
    page = request.args.get('page', 1, type=int)
    count = request.args.get('count', ROWS_PER_PAGE, type=int)

    search_dict = request.args.copy()

    if 'page' in search_dict:
        search_dict.pop('page')

    if 'count' in search_dict:
        search_dict.pop('count')

    products = Product.query.filter_by(**search_dict).paginate(page=page, per_page=count)

    return jsonify({'products': list(map(row_to_json, products))})

@app.route('/aggregate_unique', methods=['GET'])
def aggregate_unique():
    field = request.args.get('field', None)
    if field == 'Product_Name':
        vals = Product.query.group_by(Product.Product_Name).all()
        unique_vals = [val.Product_Name for val in vals]

        return jsonify({'values': unique_vals})
    elif field == 'Brand_Name':
        vals = Product.query.group_by(Product.Brand_Name).all()
        unique_vals = [val.Product_Name for val in vals]

        return jsonify({'values': unique_vals})
    else:
        return jsonify({})

@app.route('/issues', methods=['GET'])
def get_issues():
    pass

