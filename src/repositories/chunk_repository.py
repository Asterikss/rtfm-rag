from __future__ import annotations
from dataclasses import dataclass
from typing import List, TYPE_CHECKING

from result import Err, Ok, Result

if TYPE_CHECKING:
  import psycopg
  from psycopg import AsyncConnection


@dataclass
class ChunkRetriveData:
  id: int
  distance: float
  content: str
  url: str


# conn: psycopg.Connection, new_embedding: List[float], index_id: int, top_k: int = 10, conn =
async def find_closest_chunks(
  conn: AsyncConnection,
  new_embedding: List[float],
  index_id: int,
  top_k: int = 10,
) -> Result[List[ChunkRetriveData], str]:
  """
  Returns a list of ChunkRetriveData (chunk_id, distance, content) for k closest chunks.
  """
  try:
    async with conn.cursor() as cur:
      await cur.execute(
        """
        SELECT id, embedding <=> %s::vector AS distance, content, url
        FROM (
            SELECT * FROM chunks WHERE index_id = %s
        ) AS filtered_chunks
        ORDER BY embedding <=> %s::vector
        LIMIT %s;
        """,
        (new_embedding, index_id, new_embedding, top_k),
      )
      rows = await cur.fetchall()
      chunk_retrive_data_list: List[ChunkRetriveData] = [
        ChunkRetriveData(id=row[0], distance=row[1], content=row[2], url=row[3])
        for row in rows
      ]
      return Ok(chunk_retrive_data_list)
  except Exception as e:
    return Err(f"Exception in find_closest_chunks: {e}")


def insert_chunk(
  conn: psycopg.Connection,
  content: str,
  embedding: List[float],
  url: str,
  index_id: int,
) -> Result[None, str]:
  try:
    with conn.cursor() as cur:
      cur.execute(
        "INSERT INTO chunks (content, embedding, url, index_id) VALUES (%s, %s, %s, %s)",
        (content, embedding, url, index_id),
      )
    return Ok(None)
  except Exception as e:
    conn.rollback()
    return Err(f"Exception in insert_chunk: {e}")
