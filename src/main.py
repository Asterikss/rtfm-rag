from typing import Union

from fastapi import FastAPI
import uvicorn

from core.config import settings
from .core.logging_config import setup_logging

setup_logging()

app = FastAPI(title=settings.PROJECT_NAME, version=settings.API_VERSION)


@app.get("/", tags=["Root"])
async def read_root():
  return {"message": f"{settings.PROJECT_NAME} it is."}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
  return {"item_id": item_id, "q": q}


if __name__ == "__main__":
  uvicorn.run(
    "src.main:app",
    host=settings.SERVER_HOST,
    port=settings.SERVER_PORT,
    reload=settings.SERVER_DEBUG_MODE,
  )
