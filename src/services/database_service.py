from dataclasses import dataclass
from functools import lru_cache

import psycopg
from result import Err, Ok, Result

from ..core.config import config


@dataclass
class _DatabaseConfig:
  host: str = config.DB_HOST
  port: int = config.DB_PORT
  database: str = config.DB_NAME
  user: str = config.DB_USER
  password: str = config.DB_PASSWORD

  def get_connection_string(self) -> str:
    return (
      f"host={self.host} port={self.port} dbname={self.database} "
      f"user={self.user} password={self.password}"
    )


@lru_cache(maxsize=1)
def get_database_config() -> _DatabaseConfig:
  return _DatabaseConfig()


def get_database_connection() -> Result[psycopg.Connection, str]:
  try:
    conn = psycopg.connect(get_database_config().get_connection_string())
    return Ok(conn)
  except Exception as e:
    return Err(f"Failed to connect to database: {e}")
