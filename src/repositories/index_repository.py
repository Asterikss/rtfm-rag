from __future__ import annotations
from typing import List, TYPE_CHECKING, Tuple

from result import Err, Ok, Result

if TYPE_CHECKING:
  import psycopg


def get_index_id_by_name(
  conn: psycopg.Connection, index_name: str
) -> Result[int | None, str]:
  try:
    with conn.cursor() as cur:
      cur.execute(
        "SELECT id FROM indexes WHERE name = %s",
        (index_name,),
      )
      if not (row := cur.fetchone()):
        return Ok(None)
      return Ok(row[0])
  except Exception as e:
    return Err(f"Exception in get_chunk_id_by_name: {e}")


def get_indexes_state(conn: psycopg.Connection) -> Result[Tuple[int, List[str]], str]:
  """Return a tuple: (number of indexes, list of index names)."""
  try:
    with conn.cursor() as cur:
      cur.execute("SELECT name FROM indexes")
      rows = cur.fetchall()
      names = [row[0] for row in rows]
      return Ok((len(names), names))
  except Exception as e:
    return Err(f"Exception in get_indexes_info: {e}")


def create_index(
  conn: psycopg.Connection, index_name: str, source_url: str
) -> Result[int, str]:
  """Create new index in database and return its ID."""
  try:
    with conn.cursor() as cur:
      cur.execute(
        "INSERT INTO indexes (name, source_url) VALUES (%s, %s) RETURNING id",
        (index_name, source_url),
      )
      row = cur.fetchone()
      if not row:
        conn.rollback()
        return Err(f"Failed in create_index: No row returned")
      return Ok(row[0])
  except Exception as e:
    conn.rollback()
    return Err(f"Failed in create_index: {e}")


def check_index_exists(conn: psycopg.Connection, index_name: str) -> Result[bool, str]:
  try:
    with conn.cursor() as cur:
      cur.execute("SELECT COUNT(*) FROM indexes WHERE name = %s", (index_name,))
      row = cur.fetchone()
      if not row:
        conn.rollback()
        return Err(f"Failed in check_index_exists: No row returned")
      return Ok(row[0] > 0)
  except Exception as e:
    return Err(f"Failed in check_index_exists: {e}")
