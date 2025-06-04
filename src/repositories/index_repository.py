import psycopg
from result import Err, Ok, Result


def get_chunk_id_by_name(conn: psycopg.Connection, index_name: str) -> Result[int, str]:
  try:
    with conn.cursor() as cur:
      cur.execute(
        """
        SELECT id
        FROM indexes
        WHERE name = %s
        """,
        (index_name,),
      )
      if not (row := cur.fetchone()):
        return Err("Nothing fetched from get_chunk_id_by_name")
      return Ok(row[0])
  except Exception as e:
    return Err(f"Exception in get_chunk_id_by_name: {e}")
