from fastapi import FastAPI, Depends, HTTPException
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
    article = await db.create_article(article_schema=article_schema, db_session=db_session)
    return article


@app.get('/api/v1/articles/{article_id}', response_model=schemas.ArticleResponse)
async def get_article(article_id: str, db_session: AsyncSession = Depends(get_db_session)) -> models.Article | None:
    article = await db.get_article(article_id=article_id, db_session=db_session)
    if not article:
        raise HTTPException(status_code=404, detail='not found')
    return article


@app.get('/api/v1/articles', response_model=list[schemas.ArticleResponse])
async def get_articles(db_session: AsyncSession = Depends(get_db_session)) -> list[models.Article]:
    articles = await db.get_articles(db_session=db_session)
    return articles
