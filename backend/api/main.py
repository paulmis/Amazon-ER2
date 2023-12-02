from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from typing import List

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    Product_Name = db.Column(db.String(255))
    Brand_Name = db.Column(db.String(255))
    Price = db.Column(db.Float)
    Rating = db.Column(db.Integer)
    Reviews = db.Column(db.Text)
    Review_Votes = db.Column(db.Integer)

@app.route('/products', methods=['GET'])
def get_products():
    brand_name = request.args.get('brand_name')
    
    if brand_name:
        products = Product.query.filter_by(Brand_Name=brand_name).all()
    else:
        products = Product.query.all()

    product_list = []
    for product in products:
        product_data = {
            'id': product.id,
            'Product Name': product.Product_Name,
            'Brand Name': product.Brand_Name,
            'Price': product.Price,
            'Rating': product.Rating,
            'Reviews': product.Reviews,
            'Review Votes': product.Review_Votes
        }
        product_list.append(product_data)

    return jsonify({'products': product_list})

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
