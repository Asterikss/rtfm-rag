from typing import List, Tuple

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from result import Err, Ok, Result

from ....repositories.index_repository import get_indexes_state
from ....services.database_service import get_database_connection

router = APIRouter(prefix="/info")


class IndexesInfoResponseSchema(BaseModel):
  numberOfIndexes: int
  indexesNames: List[str]


def _get_indexes_info() -> Result[IndexesInfoResponseSchema, str]:
  db_conn_result: Result = get_database_connection()
  if isinstance(db_conn_result, Err):
    return Err(db_conn_result.err())

  indexes_info_result: Result[Tuple[int, List[str]], str] = get_indexes_state(
    db_conn_result.ok()
  )

  match indexes_info_result:
    case Ok(indexes_info):
      return Ok(
        IndexesInfoResponseSchema(
          numberOfIndexes=indexes_info[0], indexesNames=indexes_info[1]
        )
      )
    case Err(e):
      return Err(e)


@router.get("/indexes", response_model=IndexesInfoResponseSchema)
async def get_indexes_info():
  try:
    match _get_indexes_info():
      case Ok(result):
        return result
      case Err(e):
        raise HTTPException(status_code=400, detail=(e))
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))


@router.get("/state")
async def get_state_info():
  # TODO: todo
  try:
    raise
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
