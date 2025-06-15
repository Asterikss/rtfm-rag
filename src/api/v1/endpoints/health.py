from fastapi import APIRouter, Depends

from ....services.database_service import get_db_conn

router = APIRouter()


@router.get("/healthz", tags=["Health"])
async def healthz(conn=Depends(get_db_conn)):
  await conn.execute("SELECT 1")
  return {"status": "ok"}
