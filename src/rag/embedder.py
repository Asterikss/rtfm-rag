from __future__ import annotations
from typing import List, TYPE_CHECKING

from result import Err, Ok, Result

from ..core.constants import rag

if TYPE_CHECKING:
  from openai import OpenAI


def embed_data(openai_client: OpenAI, text: str) -> Result[List[float], str]:
  try:
    response = openai_client.embeddings.create(model=rag.EMBEDDING_MODEL, input=text)
    return Ok(response.data[0].embedding)
  except Exception as e:
    return Err(f"Failed to generate an embedding: {e}")
