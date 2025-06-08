from typing import List

from openai import OpenAI
import psycopg
from result import Err, Ok, Result

from .embedder import embed_data
from .generator import generate_response

from ..api.v1.schemas import MessageResponseSchema, MessageSchema
from ..core.constants import rag
from ..repositories.chunk_repository import ChunkRetriveData, find_closest_chunks
from ..repositories.index_repository import get_chunk_id_by_name
from ..services.database_service import get_database_connection
from ..services.openai_service import get_openai_client


def rag_pipeline(
  message_schema: MessageSchema,
) -> Result[MessageResponseSchema, str]:
  db_conn_result: Result[psycopg.Connection, str] = get_database_connection()
  if isinstance(db_conn_result, Err):
    return Err(db_conn_result.err())

  get_chunk_id_result: Result[int, str] = get_chunk_id_by_name(
    db_conn_result.ok(), message_schema.indexName
  )
  if isinstance(get_chunk_id_result, Err):
    return Err(get_chunk_id_result.err())

  openai_client_result: Result[OpenAI, str] = get_openai_client()
  if isinstance(openai_client_result, Err):
    return Err(openai_client_result.err())

  embed_result: Result[List[float], str] = embed_data(
    openai_client_result.ok(), message_schema.text
  )
  if isinstance(embed_result, Err):
    return Err(embed_result.err())

  retrived_chunks_result: Result[List[ChunkRetriveData], str] = find_closest_chunks(
    db_conn_result.ok(), embed_result.ok(), get_chunk_id_result.ok()
  )
  if isinstance(retrived_chunks_result, Err):
    return Err(retrived_chunks_result.err())

  filtered_chunks: List[ChunkRetriveData] = [
    chunk_data
    for chunk_data in retrived_chunks_result.ok()
    if chunk_data.distance < rag.MAX_RELEVANT_DISTANCE
  ]

  response_result: Result[str, str] = generate_response(
    message_schema.text, filtered_chunks
  )
  if isinstance(response_result, Err):
    return Err(response_result.err())

  links: List[str] = list(set(chunk_data.url for chunk_data in filtered_chunks))

  return Ok(MessageResponseSchema(text=response_result.ok(), links=links))
