import boto3
from .utils import bedrock, print_ww
from langchain.embeddings import BedrockEmbeddings
import numpy as np
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor, as_completed
from sqlalchemy.exc import IntegrityError
from ..models import Embedding_Cache
from .. import app, db

boto3_bedrock = bedrock.get_bedrock_client(
    region="us-east-1",
)


@lru_cache(maxsize=None)
def get_embedding(text: str):
    """Get the embedding for a given text string with caching to database."""
    with app.app_context():
        # Check for cached embedding
        cached_embedding = Embedding_Cache.query.filter_by(text=text).first()
        if cached_embedding:
            return cached_embedding.embedding

        # Generate embedding if not cached
        bedrock_embeddings = BedrockEmbeddings(
            model_id="amazon.titan-embed-text-v1", client=boto3_bedrock
        )
        embedding = bedrock_embeddings.embed_query(text)

        # Cache the new embedding
        try:
            new_cache_entry = Embedding_Cache(text=text, embedding=embedding)
            db.session.add(new_cache_entry)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            # Handle the race condition here by re-querying the database
            return Embedding_Cache.query.filter_by(text=text).first().embedding

        return embedding


def get_similarity(text1: str, text2: str):
    """Get the similarity between two text strings"""
    embedding1 = get_embedding(text1)
    embedding2 = get_embedding(text2)
    return np.dot(embedding1, embedding2)


def generate_embeddings_parallel(texts: list) -> np.ndarray:
    """Generate embeddings for a list of text strings in parallel"""
    with ThreadPoolExecutor() as executor:
        embeddings = list(executor.map(get_embedding, texts))

    return np.array(embeddings)
