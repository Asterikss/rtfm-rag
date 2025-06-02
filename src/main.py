from fastapi import FastAPI

from api.v1.endpoints.ingest import router as ingest_router
from core.config import settings
from core.logging_config import setup_logging

setup_logging()

app = FastAPI(
  title=settings.PROJECT_NAME,
  version=settings.API_VERSION,
  openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

app.include_router(
  ingest_router, prefix=settings.API_V1_STR, tags=["Ingest Operations"]
)


@app.get("/", tags=["Root"])
async def read_root():
  return {"message": f"{settings.PROJECT_NAME} it is."}


if __name__ == "__main__":
  import uvicorn

  uvicorn.run(
    "main:app",
    host=settings.SERVER_HOST,
    port=settings.SERVER_PORT,
    reload=settings.SERVER_DEBUG_MODE,
  )
