from issue_extractor import *

import sys
sys.path.append('..')
from api.models import Comment, LLM_Result
sys.path.append('../ai')

def analyze_comments(comments: list[Comment]) -> list[LLM_Result]:
    """Analyzes a list of comments and returns a list of LLM_Results."""
    df = comments_to_pd(comments)
    comment_ids = [comment.id for comment in comments]
    llm_outputs = compute_issues_for_reviews(df)
    
    return [
        llm_output_to_llm_result(llm_output, comment_id)
        for llm_output, comment_id in zip(llm_outputs, comment_ids)
    ]
    
def cluster_llm_results(llm_results: list[LLM_Result]) -> dict[str, str]:
    """Clusters a list of LLM_Results and returns a list of LLM_Results."""
    df = llm_results_to_pd(llm_results)
    return cluster_issues_for_reviews(df)
    
#######################
# Helper Functions  ### 
#######################

def comments_to_pd(comments: list[Comment]) -> pd.DataFrame:
    """Converts a list of comments to a pandas DataFrame."""

    return pd.DataFrame(
        data=[
            [
                comment.product,
                comment.brand,
                comment.price,
                comment.rating,
                comment.review,
                comment.votes,
            ]
            for comment in comments
        ],
        columns=["Product Name", "Brand Name", "Price", "Rating", "Reviews", "Review Votes"],
    )

def llm_output_to_llm_result(llm_output: dict, comment_id: int) -> LLM_Result:
    """Converts a LLM_Output to a LLM_Result."""
    return LLM_Result(
        issues=llm_output["issues"],
        comment_id=comment_id,
    )

def llm_results_to_pd(llm_results: list[LLM_Result]) -> pd.DataFrame:
    """Converts a list of LLM_Results to a pandas DataFrame."""
    return pd.DataFrame(
        data=[
            [
                {"issues": llm_result.issues},
            ]
            for llm_result in llm_results
        ],
        columns=["LLM_OUTPUT"],
    )

    
    