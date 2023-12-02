from issue_extractor import *

# Comment(db.Model) resides in ../backend/api/models.py
from ..backend.api.models import Comment, LLM_Result


def comments_to_pd(comments: list[Comment]) -> pd.DataFrame:
    """Converts a list of comments to a pandas DataFrame."""
    # comment.product -> Product Name
    # comment.brand -> Brand Name
    # comment.price -> Price
    # comment.rating -> Rating
    # comment.review -> Reviews
    # comment.votes -> Review Votes

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
def analyze_comments(comments: list[Comment]) -> list[LLM_Result]:
    """Analyzes a list of comments and returns a list of LLM_Results."""
    df = comments_to_pd(comments)
    comment_ids = [comment.id for comment in comments]
    llm_outputs = compute_issues_for_reviews(df)
    
    return [
        llm_output_to_llm_result(llm_output, comment_id)
        for llm_output, comment_id in zip(llm_outputs, comment_ids)
    ]
    

def llm_results_to_pd(llm_results: list[LLM_Result]) -> pd.DataFrame:
    """Converts a list of LLM_Results to a pandas DataFrame."""
    return pd.DataFrame(
        data=[
            [
                llm_result.issues,
                llm_result.severities,
                llm_result.comment,
            ]
            for llm_result in llm_results
        ],
        columns=["LLM_OUTPUT"],
    )
    
def cluster_llm_results(llm_results: list[LLM_Result]) -> dict[str, str]:
    """Clusters a list of LLM_Results and returns a list of LLM_Results."""
    df = llm_results_to_pd(llm_results)
    return cluster_issues_for_reviews(df)
    
    
    