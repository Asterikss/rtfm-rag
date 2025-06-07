from dataclasses import dataclass
from typing import List

import psycopg
from result import Err, Ok, Result


@dataclass
class ChunkRetriveData:
  id: int
  distance: float
  content: str
  url: str


def find_closest_chunks(
  conn: psycopg.Connection, new_embedding: List[float], index_id: int, top_k: int = 10
) -> Result[List[ChunkRetriveData], str]:
  """
  Returns a list of ChunkRetriveData (chunk_id, distance, content) for k closest chunks.
  """
  try:
    with conn.cursor() as cur:
      cur.execute(
        """
        SELECT id, embedding <-> %s::vector AS distance, content, url
        FROM chunks
        WHERE index_id = %s
        ORDER BY embedding <-> %s::vector
        LIMIT %s
        """,
        (new_embedding, index_id, new_embedding, top_k),
      )
      rows = cur.fetchall()
      chunk_retrive_data_list: List[ChunkRetriveData] = [
        ChunkRetriveData(id=row[0], distance=row[1], content=row[2], url=row[3])
        for row in rows
      ]
      return Ok(chunk_retrive_data_list)
  except Exception as e:
    return Err(f"Failed when trying to find closest chunks {e}")
