from fastapi import APIRouter, Depends

from ....core.config import config
from ....services.database_service import get_db_conn

router = APIRouter()


@router.get("/healthz")
async def healthz(conn=Depends(get_db_conn)):
  await conn.execute("SELECT 1")
  return {"status": "ok"}


@router.get("/checkz")
async def read_root():
  return {f"{config.PROJECT_NAME}": "it is"}
