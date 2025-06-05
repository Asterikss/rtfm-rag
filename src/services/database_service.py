from functools import lru_cache

import psycopg
from result import Err, Ok, Result

from ..core.config import config


class _DatabaseConfig:
  def __init__(
    self,
    host: str = config.DB_HOST,
    port: int = config.DB_PORT,
    database: str = config.DB_NAME,
    user: str = config.DB_USER,
    password: str = config.DB_PASSWORD,
  ):
    self.host = host
    self.port = port
    self.database = database
    self.user = user
    self.password = password

  def get_connection_string(self) -> str:
    return f"host={self.host} port={self.port} dbname={self.database} user={self.user} password={self.password}"


@lru_cache(maxsize=1)
def get_database_config() -> _DatabaseConfig:
  return _DatabaseConfig()


def get_database_connection() -> Result[psycopg.Connection, str]:
  try:
    conn = psycopg.connect(get_database_config().get_connection_string())
    return Ok(conn)
  except Exception as e:
    return Err(f"Failed to connect to database: {e}")
