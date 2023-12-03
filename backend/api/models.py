from sqlalchemy import PickleType
from . import db
from typing import Dict, Optional, Any
from sqlalchemy.orm import Mapped, relationship


class LLM_Result(db.Model):
    id: int = db.Column(
        db.Integer, primary_key=True, autoincrement=True, nullable=False
    )
    comment_id: int = db.Column(
        db.Integer,
        db.ForeignKey("comment.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )
    issues: Dict[Any, Any] = db.Column(PickleType)
    issue_count: int = db.Column(db.Integer)

    comment = relationship("Comment", back_populates="llm_result")

    def __init__(self, issues, comment_id):
        self.issues = issues
        self.comment_id = comment_id
        self.issue_count = len(issues)


class Comment(db.Model):
    id: int = db.Column(
        db.Integer, primary_key=True, autoincrement=True, nullable=False
    )
    product: str = db.Column(db.String(255), index=True)
    brand: str = db.Column(db.String(255), index=True)
    price: float = db.Column(db.Float)
    rating: int = db.Column(db.Integer)
    review: str = db.Column(db.Text)
    votes: int = db.Column(db.Integer)
    llm_result: Mapped[LLM_Result] = relationship(
        "LLM_Result", uselist=False, back_populates="comment"
    )

    def __init__(self, product, brand, price, rating, review, votes):
        self.product = product
        self.brand = brand
        self.price = price
        self.rating = rating
        self.review = review
        self.votes = votes


class LLM_Cache(db.Model):
    id: int = db.Column(
        db.Integer, primary_key=True, autoincrement=True, nullable=False
    )
    text_prompt: str = db.Column(db.Text, unique=True, nullable=False)
    llm_response: str = db.Column(db.Text, nullable=False)

    def __init__(self, text_prompt, llm_response):
        self.text_prompt = text_prompt
        self.llm_response = llm_response


class Embedding_Cache(db.Model):
    id: Mapped[int] = db.Column(
        db.Integer, primary_key=True, autoincrement=True, nullable=False
    )
    text: Mapped[str] = db.Column(db.Text, unique=True, nullable=False)
    embedding: Mapped[Any] = db.Column(PickleType, nullable=False)

    def __init__(self, text, embedding):
        self.text = text
        self.embedding = embedding
