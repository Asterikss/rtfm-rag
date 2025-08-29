#!/usr/bin/env python3
"""
MCP server exposing get_docs_context tool
Run with: python -m src.mcp.mcp_server
"""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass

from mcp.server.fastmcp import Context, FastMCP
from mcp.server.session import ServerSession
from psycopg import AsyncConnection
from result import Err, Ok, Result

from src.mcp.mcp_tools import fetch_docs_candidate_context_impl
from src.services.database_service import get_db_connection_string


@dataclass
class AppContext:
  db_conn: AsyncConnection


@asynccontextmanager
async def lifespan(_: FastMCP) -> AsyncIterator[AppContext]:
  conn = await AsyncConnection.connect(get_db_connection_string())
  try:
    yield AppContext(db_conn=conn)
  finally:
    await conn.close()


mcp = FastMCP(name="rtfm-rag-mcp", lifespan=lifespan, host="0.0.0.0", port=8033)


@mcp.tool()
async def fetch_docs_candidate_context(
  query: str, index_name: str, ctx: Context[ServerSession, AppContext]
) -> str:
  """Retrieve context from the specified docs index based on query similarity."""
  context_result: Result[str, str] = await fetch_docs_candidate_context_impl(
    query, index_name, ctx.request_context.lifespan_context.db_conn
  )
  match context_result:
    case Ok(context):
      return context
    case Err(e):
      return f"Getting context failed: {e}"


if __name__ == "__main__":
  print("Starting the rtfm-rag-mcp server")
  mcp.run(transport="stdio")
