import boto3
from .utils import bedrock, print_ww
from langchain.embeddings import BedrockEmbeddings
import numpy as np
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor, as_completed
from .embeddings import generate_embeddings_parallel
from .llm import llm_wrapper
import os
import json
from .prompts import *
import time
import pandas as pd
from sklearn.cluster import OPTICS

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
    
    # We now have json and we need to add the embeddings of the issue names for every single issue.
    # We flatten the issues into a list
    llm_outputs = results
    issues = []
    for llm_output in llm_outputs:
        issues.extend(llm_output['issues'])
    
    # Issue names
    issue_names = [issue['issue'] for issue in issues]
    
    # We generate the embeddings for the issue names
    embeddings_issue_names = generate_embeddings_parallel(issue_names)
    issue_name_to_embedding = dict(zip(issue_names, embeddings_issue_names))
    # We add the embeddings to the issues
    for llm_output in llm_outputs:
        for issue in llm_output['issues']:
            issue['embedding'] = issue_name_to_embedding[issue['issue']]
    
    return llm_outputs

def cluster_issues_for_reviews(product_reviews: pd.DataFrame):
    if 'LLM_OUTPUT' not in product_reviews.columns:
        raise ValueError("LLM_OUTPUT column not found")
    
    # We flatten the issues into a list
    llm_outputs = product_reviews['LLM_OUTPUT'].tolist()
    # Get all issue names and their embeddings
    issues = []
    for llm_output in llm_outputs:
        issues.extend(llm_output['issues'])
    
    # Issue names
    issue_names = [issue['issue'] for issue in issues]
    
    # Embeddings of issue names
    embeddings_issue_names = np.array([issue['embedding'] for issue in issues])
    
    # OPTICS Clustering
    clustering = OPTICS(metric='cosine', min_samples=min(5,len(embeddings_issue_names))).fit(embeddings_issue_names)
    labels = clustering.labels_
    
    # We group the issues by cluster
    clusters = {}
    for i, label in enumerate(labels):
        if label == -1:
            continue
        if label not in clusters:
            clusters[label] = []
        clusters[label].append(issues[i])
    
    # For each cluster we get the center
    clusters_centers = {}
    for cluster in clusters:
        cluster_embeddings = np.array([issue['embedding'] for issue in clusters[cluster]])
        clusters_centers[cluster] = np.mean(cluster_embeddings, axis=0)
    
    # We get for each cluster the closest issue name to the cluster center
    clusters_issue_names = {}
    for cluster in clusters_centers:
        cluster_center = clusters_centers[cluster]
        distances = np.linalg.norm(cluster_center - embeddings_issue_names, axis=1)
        closest_issue_index = np.argmin(distances)
        clusters_issue_names[cluster] = issue_names[closest_issue_index]
    
    # We now go from cluster_issue_name to all issues names in the cluster
    clusters_issues = {}
    for cluster in clusters_issue_names:
        clusters_issues[clusters_issue_names[cluster]] = [issue['issue'] for issue in clusters[cluster]]
    
    return clusters_issues

    
    
    
    
    
