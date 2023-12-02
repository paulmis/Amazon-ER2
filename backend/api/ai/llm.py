import numpy as np
import json
from anthropic_bedrock import AnthropicBedrock
import anthropic_bedrock
import os
from functools import lru_cache

client = AnthropicBedrock(
    aws_access_key=os.environ["AWS_ACCESS_KEY_ID"],
    aws_secret_key=os.environ["AWS_SECRET_ACCESS_KEY"],
)

@lru_cache(maxsize=None)
def llm_wrapper(text: str) -> str:
    """Wrapper for the LLM API"""
    return client.completions.create(
        model="anthropic.claude-v2:1",
        max_tokens_to_sample=1024,
        prompt=f"{text}"
    ).completion
