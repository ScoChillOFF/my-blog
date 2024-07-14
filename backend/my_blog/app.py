import asyncio
import sys

from fastapi import FastAPI, HTTPException, Query

from typing import Annotated

from .dependencies import DBSession
from .db_api import schemas, models
from .db_api import crud as db


app = FastAPI()

# Boilerplate for Windows
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
# ------------------------


@app.get('/api/v1/ping')
async def ping() -> dict[str, str]:
    return {'status': 'ok'}


@app.post('/api/v1/articles', response_model=schemas.ArticleResponse)
async def create_article(article_schema: schemas.ArticleCreation, db_session: DBSession) -> models.Article:
    article = await db.create_article(article_schema=article_schema, db_session=db_session)
    return article


@app.get('/api/v1/articles/{article_id}', response_model=schemas.ArticleResponse)
async def get_article(article_id: str, db_session: DBSession) -> models.Article:
    article = await db.get_article(article_id=article_id, db_session=db_session)
    if not article:
        raise HTTPException(status_code=404, detail='not found')
    return article


@app.get('/api/v1/articles', response_model=list[schemas.ArticleResponse])
async def get_articles(db_session: DBSession, days_limit: int | None = None, tags: Annotated[list[str] | None, Query()] = None) -> list[models.Article]:
    articles = await db.get_articles(db_session=db_session, days_limit=days_limit, tag_names=tags)
    return articles


@app.delete('/api/v1/articles/{article_id}')
async def delete_article(article_id: str, db_session: DBSession) -> dict[str, str]:
    await db.delete_article(article_id=article_id, db_session=db_session)
    return {'status': 'ok'}


@app.put('/api/v1/articles/{article_id}', response_model=schemas.ArticleResponse)
async def update_article(article_id: str, article_schema: schemas.ArticleUpdating, db_session: DBSession) -> models.Article:
    article = await db.update_article(article_id=article_id, article_schema=article_schema, db_session=db_session)
    if not article:
        raise HTTPException(status_code=404, detail='not found')
    return article
