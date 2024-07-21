from fastapi import APIRouter

from ..db_api import models, schemas, crud as db
from ..dependencies import DBSession


router = APIRouter()


@router.get("/api/v1/tags", response_model=list[schemas.TagResponse])
async def get_tags(db_session: DBSession) -> list[models.Tag]:
    tags = await db.get_tags(db_session)
    return tags
