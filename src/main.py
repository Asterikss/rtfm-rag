from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.v1.endpoints.ingest import router as ingest_router
from .api.v1.endpoints.query import router as query_router
from .core.config import config

app = FastAPI(
  title=config.PROJECT_NAME,
  version=config.API_VERSION,
  openapi_url=f"{config.API_V1_STR}/openapi.json",
)

app.add_middleware(
  CORSMiddleware,
  allow_origins=[
    "http://localhost:5173",
    "http://127.0.0.1:5173",
  ],
  allow_credentials=True,
  allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
  allow_headers=["*"],
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
