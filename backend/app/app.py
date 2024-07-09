from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .dependencies import get_db_session
from .db_api import schemas, models
from .db_api import crud as db


app = FastAPI()


@app.get('/api/v1/ping')
async def ping() -> dict[str, str]:
    return {'status': 'ok'}


@app.post('/api/v1/articles', response_model=schemas.ArticleResponse)
async def create_article(article_schema: schemas.ArticleCreation, db_session: AsyncSession = Depends(get_db_session)) -> models.Article:
    article_response = await db.create_article(article_schema=article_schema, db_session=db_session)
    return article_response
