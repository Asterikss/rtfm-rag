from typing import List
from result import Err, Ok, Result

from ..repositories.chunk_repository import ChunkRetriveData
from ..services.openai_service import get_openai_client
from ..core.constants import rag


def generate_response(query: str, chunks: List[ChunkRetriveData]) -> Result[str, str]:
  # TODO: possibly utilize links
  openai_clinet_result = get_openai_client()
  if isinstance(openai_clinet_result, Err):
    return Err(openai_clinet_result.err())

  context_list: List[str] = []
  for chunk in chunks:
    context_list.append(chunk.content)

  context = "\n\n".join(context_list)

  content = rag.GENERATOR_USER_PROMPT_TEMPLATE.replace("{context}", context).replace(
    "{user_query}", query
  )

  try:
    response = openai_clinet_result.ok().responses.create(
      model="gpt-4.1-mini",
      temperature=0.2,
      instructions=rag.GENERATOR_SYSTEM_PROMPT,
      max_output_tokens=1000,
      input=[
        {
          "role": "user",
          "content": content,
        }
      ],
    )
    return Ok(response.output_text)
  except Exception as e:
    return Err(f"Exception occured when trying to generate an llm answer: {e}")
