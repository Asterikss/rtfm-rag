from typing import List, TYPE_CHECKING

from result import Err, Ok, Result, UnwrapError

from ..api.v1.schemas import MessageResponseSchema, MessageSchema
from ..core.constants import rag
from ..repositories.chunk_repository import ChunkRetriveData, find_closest_chunks
from ..repositories.index_repository import get_chunk_id_by_name
from ..services.database_service import get_database_connection
from ..services.openai_service import get_openai_client
from .embedder import embed_data
from .generator import generate_response

if TYPE_CHECKING:
  from openai import OpenAI
  import psycopg


def rag_pipeline(
  message_schema: MessageSchema,
) -> Result[MessageResponseSchema, str]:
  try:
    db_conn: psycopg.Connection = get_database_connection().unwrap()

    get_chunk_id: int = get_chunk_id_by_name(db_conn, message_schema.indexName).unwrap()

    openai_client: OpenAI = get_openai_client().unwrap()

    embedding: List[float] = embed_data(openai_client, message_schema.text).unwrap()

    retrived_chunks: List[ChunkRetriveData] = find_closest_chunks(
      db_conn, embedding, get_chunk_id
    ).unwrap()

    filtered_chunks: List[ChunkRetriveData] = [
      chunk_data
      for chunk_data in retrived_chunks
      if chunk_data.distance < rag.MAX_RELEVANT_DISTANCE
    ]

    response: str = generate_response(message_schema.text, filtered_chunks).unwrap()

    links: List[str] = list(set(chunk_data.url for chunk_data in filtered_chunks))

    return Ok(MessageResponseSchema(text=response, links=links))
  except UnwrapError as e:
    return Err(str(e))
