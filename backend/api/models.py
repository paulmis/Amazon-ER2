from sqlalchemy import PickleType
from . import db
from typing import Dict, Optional, Any
from sqlalchemy.orm import Mapped, relationship

class LLM_Result(db.Model):
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    comment_id: int = db.Column(db.Integer, db.ForeignKey('comment.id', ondelete='CASCADE'), unique=True, nullable=False)
    issues: Dict[Any, Any] = db.Column(PickleType)

    comment = relationship('Comment', back_populates='llm_result')

    def __init__(self, issues, severities, comment):
        self.issues = issues
        self.severities = severities
        self.comment = comment

class Comment(db.Model):
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    product: str = db.Column(db.String(255), index=True)
    brand: str = db.Column(db.String(255), index=True)
    price: float = db.Column(db.Float)
    rating: int = db.Column(db.Integer)
    review: str = db.Column(db.Text)
    votes: int = db.Column(db.Integer)
    llm_result: Mapped[LLM_Result] = relationship('LLM_Result', uselist=False, back_populates='comment')

    def __init__(self, product, brand, price, rating, review, votes):
        self.product = product
        self.brand = brand
        self.price = price
        self.rating = rating
        self.review = review
        self.votes = votes
