import boto3
from utils import bedrock, print_ww
from langchain.embeddings import BedrockEmbeddings
import numpy as np
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor, as_completed
from embeddings import generate_embeddings_parallel
from llm import llm_wrapper
import os
import json
from prompts import *
import time
import pandas as pd

def get_json_from_comment_analysis(comment_analysis: str) -> dict:
    """
    Get the json from the comment analysis
    """
    try:
        start = comment_analysis.find("```")
        if start == -1:
            raise ValueError("No code block found")

        end = comment_analysis.find("```", start + 3)
        if end == -1:
            raise ValueError("No closing code block found")

        json_string = comment_analysis[start + 3:end].strip()

        if json_string.startswith("json"):
            json_string = json_string[4:].strip()

        return json.loads(json_string)

    except ValueError as ve:
        raise ve
    except Exception as e:
        raise ValueError("Invalid or not JSON format") from e
    
def get_json_for_comment(product_name: str, comment: str, iter = 0):
    try:
        completion = llm_wrapper(create_issue_extraction_prompt(product_name, comment))
    
        return get_json_from_comment_analysis(completion)
    except ValueError as ve:
        if iter > 25:
            raise ve
        # sleep for 5 seconds
        time.sleep(5)
        return get_json_for_comment(comment, iter + 1)

def get_json_for_comment_paralllel(product_name: str, comment: str):
    return get_json_for_comment(product_name, comment)

def compute_issues_for_reviews(product_reviews: pd.DataFrame, max_workers=100):
    # Create a list to store the futures
    futures = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for row in product_reviews.itertuples():
            future = executor.submit(get_json_for_comment_paralllel, row[1], row[5])  
            futures.append(future)

        results = [future.result() for future in futures]
    
    return results


def cluster_issues_for_reviews(product_reviews: pd.DataFrame, max_workers=100):
    if 'LLM_OUTPUT' not in product_reviews.columns:
        raise ValueError("LLM_OUTPUT column not found")
    
    if 
    
    
    
    
    