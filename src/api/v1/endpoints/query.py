from fastapi import APIRouter, HTTPException
from result import Err, Ok, Result

from ....rag.pipeline import rag_pipeline
from ..schemas import MessageResponseSchema, MessageSchema

router = APIRouter()


@router.post("/query", response_model=MessageResponseSchema)
async def query(message_schema: MessageSchema):
  try:
    result: Result[MessageResponseSchema, str] = await rag_pipeline(message_schema)
    match result:
      case Ok(response):
        return response
      case Err(e):
        raise HTTPException(status_code=400, detail=(e))
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
