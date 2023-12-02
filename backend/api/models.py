from sqlalchemy import PickleType
from . import db
from typing import List
from sqlalchemy.orm import relationship

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    product = db.Column(db.String(255), index=True)
    brand = db.Column(db.String(255), index=True)
    price = db.Column(db.Float)
    rating = db.Column(db.Integer)
    review = db.Column(db.Text)
    votes = db.Column(db.Integer)
    llm_result = relationship('LLM_Result', uselist=False, back_populates='comment', cascade='all, delete-orphan')

    def __init__(self, product, brand, price, rating, review, votes):
        self.product = product
        self.brand = brand
        self.price = price
        self.rating = rating
        self.review = review
        self.votes = votes

class LLM_Result(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id', ondelete='CASCADE'), unique=True, nullable=False)
    issues = db.Column(PickleType)

    comment = relationship('Comment', back_populates='llm_result')

    def __init__(self, issues, severities, comment):
        self.issues = issues
        self.severities = severities
        self.comment = comment
