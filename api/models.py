from . import db
from typing import List

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    Product_Name = db.Column(db.String(255))
    Brand_Name = db.Column(db.String(255))
    Price = db.Column(db.Float)
    Rating = db.Column(db.Integer)
    Reviews = db.Column(db.Text)
    Review_Votes = db.Column(db.Integer)
