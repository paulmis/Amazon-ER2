from .issue_extractor import *

import sys
from ..models import Comment, LLM_Result

boto3_bedrock = bedrock.get_bedrock_client(
    region="us-east-1",
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


def cluster_llm_results(
    llm_results: list[LLM_Result],
) -> dict[str, list[tuple[LLM_Result, int]]]:
    """Clusters a list of LLM_Results and returns a list of LLM_Results."""

    if len(llm_results) == 0:
        return {}
    df = llm_results_to_pd(llm_results)
    clustered_issues = cluster_issues_for_reviews(df)
    inverse_clustered_issues = {}
    for issue in clustered_issues:
        for issue_name in clustered_issues[issue]:
            inverse_clustered_issues[issue_name] = issue

    final_clustered_issues = {}
    for llm_result in llm_results:
        for i, issue in enumerate(llm_result.issues):
            if issue["issue"] in inverse_clustered_issues:
                inverse_issue = inverse_clustered_issues[issue["issue"]]
                final_clustered_issues[inverse_issue] = final_clustered_issues.get(
                    inverse_issue, []
                )
                final_clustered_issues[inverse_issue].append((llm_result, i))
    return final_clustered_issues


def embbed_strings(strings: list[str]) -> list[np.ndarray]:
    """Embeds a list of strings and returns a list of embeddings."""
    return generate_embeddings_parallel(strings)


def generate_image(text: str) -> str:
    """Generates an image from a text string and returns the image as a base64 encoded string."""
    prompt = text
    negative_prompts = []
    style_preset = "photographic"  # (e.g. photographic, digital-art, cinematic, ...)
    clip_guidance_preset = (
        "FAST_GREEN"  # (e.g. FAST_BLUE FAST_GREEN NONE SIMPLE SLOW SLOWER SLOWEST)
    )
    sampler = "K_DPMPP_2S_ANCESTRAL"  # (e.g. DDIM, DDPM, K_DPMPP_SDE, K_DPMPP_2M, K_DPMPP_2S_ANCESTRAL, K_DPM_2, K_DPM_2_ANCESTRAL, K_EULER, K_EULER_ANCESTRAL, K_HEUN, K_LMS)
    width = 768
    request = json.dumps(
        {
            "text_prompts": (
                [{"text": prompt, "weight": 1.0}]
                + [
                    {"text": negprompt, "weight": -1.0}
                    for negprompt in negative_prompts
                ]
            ),
            "cfg_scale": 5,
            "seed": 452345,
            "steps": 50,
            "style_preset": style_preset,
            "clip_guidance_preset": clip_guidance_preset,
            "sampler": sampler,
            "width": width,
        }
    )
    modelId = "stability.stable-diffusion-xl"

    response = boto3_bedrock.invoke_model(body=request, modelId=modelId)
    response_body = json.loads(response.get("body").read())

    return response_body["artifacts"][0].get("base64")


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
        columns=[
            "Product Name",
            "Brand Name",
            "Price",
            "Rating",
            "Reviews",
            "Review Votes",
        ],
    )


def llm_output_to_llm_result(llm_output: dict, comment_id: int) -> LLM_Result:
    """Converts a LLM_Output to a LLM_Result."""
    return LLM_Result(
        issues=llm_output["issues"],
        comment_id=comment_id
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
