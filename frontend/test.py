import flask


app = flask.Flask(__name__)

# export interface Product {
#     id: number;
#     Product_Name: string;
#     Brand_Name: string;
#     Price: number;
#     Rating: number;
#     Reviews: string[];
#     Review_Votes: number[];
# }
class Product:
    def __init__(self, id, product_name, brand_name, price, rating, reviews, review_votes):
        self.id = id
        self.product_name = product_name
        self.brand_name = brand_name
        self.price = price
        self.rating = rating
        self.reviews = reviews
        self.review_votes = review_votes

    def to_dict(self):
        return {
            "id": self.id,
            "Product_Name": self.product_name,
            "Brand_Name": self.brand_name,
            "Price": self.price,
            "Rating": self.rating,
            "Reviews": self.reviews,
            "Review_Votes": self.review_votes,
        }
# create a get endpoint for /products
# return a list of products
def get_products():
    products: list[str] = ["iPhone 12", "ALCATEL OneTouch Idol 3 Global Unlocked 4G LTE Smartphone, 4.7 HD IPS Display, 16GB (GSM - US Warranty)", "Pixel 5"]
    # products.append(Product(1, "iPhone 12", "Apple", 799, 4.5, ["Great phone", "Awesome camera"], [10, 20]))
    # products.append(Product(2, "ALCATEL OneTouch Idol 3 Global Unlocked 4G LTE Smartphone, 4.7 HD IPS Display, 16GB (GSM - US Warranty)", "Samsung", 699, 4.0, ["Good phone", "Great screen"], [5, 10]))
    # products.append(Product(3, "Pixel 5", "Google", 599, 4.0, ["Good phone", "Great camera"], [5, 10]))
    
    return products

@app.route('/aggregate_unique', methods=['GET'])
def get_products_handler():
    page = flask.request.args.get('page', 1, type=int)
    products = get_products()
    response =  flask.jsonify(products)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


app.run(debug=True)