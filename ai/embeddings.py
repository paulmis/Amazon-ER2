import boto3
from utils import bedrock, print_ww
from langchain.embeddings import BedrockEmbeddings
import numpy as np
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor, as_completed

boto3_bedrock = bedrock.get_bedrock_client(
    region='us-east-1',
)

@lru_cache(maxsize=None)
def get_embedding(text: str):
    """Get the embedding for a given text string"""
    bedrock_embeddings = bedrock_embeddings = BedrockEmbeddings(model_id="amazon.titan-embed-text-v1", client=boto3_bedrock)
    return bedrock_embeddings.embed_query(text)

def get_similarity(text1: str, text2: str):
    """Get the similarity between two text strings"""
    embedding1 = get_embedding(text1)
    embedding2 = get_embedding(text2)
    return np.dot(embedding1, embedding2)

def generate_embeddings_parallel(texts: list):
    """Generate embeddings for a list of text strings in parallel"""
    with ThreadPoolExecutor() as executor:
        embeddings = list(executor.map(get_embedding, texts))

    return np.array(embeddings)

    