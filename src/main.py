from fastapi import FastAPI

from .api.v1.endpoints.ingest import router as ingest_router
from .api.v1.endpoints.query import router as query_router
from .core.config import config
from .core.logging_config import setup_logging

setup_logging()

app = FastAPI(
  title=config.PROJECT_NAME,
  version=config.API_VERSION,
  openapi_url=f"{config.API_V1_STR}/openapi.json",
)

app.include_router(ingest_router, prefix=config.API_V1_STR, tags=["Ingest Operations"])

app.include_router(query_router, prefix=config.API_V1_STR, tags=["Query Operations"])


@app.get("/", tags=["Root"])
async def read_root():
  return {"message": f"{config.PROJECT_NAME} it is."}


if __name__ == "__main__":
  import uvicorn

  uvicorn.run(
    "src.main:app",
    host=config.SERVER_HOST,
    port=config.SERVER_PORT,
    reload=config.SERVER_DEBUG_MODE,
  )
