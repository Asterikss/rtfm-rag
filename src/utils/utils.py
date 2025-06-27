from functools import lru_cache, wraps
from time import perf_counter
from typing import Any, Callable

import tiktoken

from ..core.constants import rag


@lru_cache(maxsize=1)
def _get_embed_model_encoding():
  return tiktoken.encoding_for_model(rag.EMBEDDING_MODEL)


def get_embed_token_count(text: str) -> int:
  return len(_get_embed_model_encoding().encode(text))


def get_time(func: Callable) -> Callable:
  @wraps(func)
  def wrapper(*args, **kwargs) -> Any:
    start_time: float = perf_counter()
    result: Any = func(*args, **kwargs)
    end_time: float = perf_counter()

    print(f"'{func.__name__}()' took {end_time - start_time:.3f} seconds to execute")
    return result

  return wrapper


def get_time_async(func: Callable) -> Callable:
  @wraps(func)
  async def wrapper(*args, **kwargs) -> Any:
    start_time = perf_counter()
    result = await func(*args, **kwargs)
    end_time = perf_counter()
    print(f'"{func.__name__}()" took {end_time - start_time:.3f} seconds to execute')
    return result

  return wrapper
