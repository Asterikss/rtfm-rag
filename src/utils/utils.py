from functools import lru_cache

import tiktoken

from ..core.constants import rag


@lru_cache(maxsize=1)
def _get_embed_model_encoding():
  return tiktoken.encoding_for_model(rag.EMBEDDING_MODEL)


def get_embed_token_count(text: str) -> int:
  return len(_get_embed_model_encoding().encode(text))
