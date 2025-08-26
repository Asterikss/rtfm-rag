#!/usr/bin/env python3
"""
MCP server for the app exposing get_docs_context tool
Run with: python -m src.mcp.mcp_server
"""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass

from mcp.server.fastmcp import Context, FastMCP
from mcp.server.session import ServerSession
from psycopg import AsyncConnection
from result import Err, Ok, Result

from src.api.v1.schemas import MessageResponseSchema, MessageSchema
from src.rag.pipeline import rag_pipeline
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


mcp = FastMCP(name="rftm-rag-mcp", lifespan=lifespan, host="0.0.0.0", port=8033)


@mcp.tool()
async def get_docs_context(
  query: str, index_name: str, ctx: Context[ServerSession, AppContext]
) -> str:
  """Get the contex from the chosen docs (index_name) given the query"""
  message = MessageSchema(text=query, indexName=index_name, userId="Yup")
  db_conn = ctx.request_context.lifespan_context.db_conn

  rag_pipeline_result: Result[MessageResponseSchema, str] = await rag_pipeline(
    message, db_conn
  )

  match rag_pipeline_result:
    case Ok(message_response):
      return message_response.text
    case Err(e):
      return f"Getting context failed: {e}"


if __name__ == "__main__":
  print("Starting the rftm-rag-mcp server")
  mcp.run(transport="stdio")
