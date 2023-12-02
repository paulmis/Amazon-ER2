from flask import jsonify, request
from . import app
from .models import Product

row_to_json = lambda row: {column: str(getattr(row, column)) for column in row.__table__.c.keys()}

@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.filter_by(**request.args).all()

    return jsonify({'products': list(map(row_to_json, products))})

@app.route('/aggregate_unique', methods=['GET'])
def aggregate_unique():
    field = request.args.get('field', None)
    if field == 'Product_Name':
        unique_vals = db.session.query(Product.Product_Name).distinct().all()
        unique_vals = [val[0] for val in vals]

        return jsonify({'values': unique_vals})
    elif field == 'Brand_Name':
        unique_vals = db.session.query(Product.Brand_Name).distinct().all()
        unique_vals = [val[0] for val in vals]

        return jsonify({'values': unique_vals})
    else:
        return jsonify({})

