from typing import List

from openai import OpenAI
from result import Result, Ok, Err

from ..core.constants import rag


def embed_data(openai_client: OpenAI, text: str) -> Result[List[float], str]:
  try:
    response = openai_client.embeddings.create(model=rag.EMBEDDING_MODEL, input=text)
    return Ok(response.data[0].embedding)
  except Exception as e:
    return Err(f"Failed to generate an embedding: {e}")
