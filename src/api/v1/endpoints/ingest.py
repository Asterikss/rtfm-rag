from typing import Dict, Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl
from result import Err, Ok, Result

from services.documentation_scraper import DocumentationScraper


router = APIRouter(prefix="/ingest")


class IngestLinkSchema(BaseModel):
  url: HttpUrl
  indexName: str


async def _ingest_link(ingest_link_schema: IngestLinkSchema) -> Result[Dict, str]:
  scraper = DocumentationScraper()
  scrape_result: Result[Dict, str] = await scraper.scrape_website(
    ingest_link_schema.url
  )
  if isinstance(scrape_result, Err):
    return Err(scrape_result.err())
  return Ok(scrape_result.ok())


@router.post("/link")
async def ingest_link(ingest_link_schema: IngestLinkSchema) -> Dict[str, Any]:
  try:
    result: Result[Dict, str] = await _ingest_link(ingest_link_schema)
    match result:
      case Ok(summary):
        return summary
      case Err(e):
        raise HTTPException(status_code=400, detail=(e))
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
