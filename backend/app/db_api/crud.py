from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa

from datetime import datetime, timezone, timedelta

from . import schemas, models


async def create_article(article_schema: schemas.ArticleCreation, db_session: AsyncSession) -> models.Article:
    article = models.Article(**article_schema.model_dump())
    db_session.add(article)
    await db_session.commit()
    await db_session.refresh(article)
    return article


async def get_article(article_id: str, db_session: AsyncSession) -> models.Article:
    article = await db_session.get(models.Article, article_id)
    return article


async def get_articles(db_session: AsyncSession, days_limit: int | None = None) -> list[models.Article]:
    query = sa.select(models.Article).order_by(models.Article.created_at.desc())
    if days_limit is not None:
        query = apply_days_limit(query, days_limit)
    result = await db_session.scalars(query)
    articles = result.all()
    return articles


def apply_days_limit(query: sa.Select, days_limit: int) -> sa.Select:
    converted_days = timedelta(days=days_limit)
    current_date = datetime.now(tz=timezone.utc).date()
    return query.where(models.Article.created_at >= current_date - converted_days)


async def delete_article(article_id: str, db_session: AsyncSession) -> None:
    article = await get_article(article_id=article_id, db_session=db_session)
    if not article:
        return
    await db_session.delete(article)
    await db_session.commit()
    return


async def update_article(article_id: str, article_schema: schemas.ArticleUpdating, db_session: AsyncSession) -> models.Article | None:
    article = await get_article(article_id=article_id, db_session=db_session)
    if not article:
        return
    
    for attribute, value in article_schema.model_dump().items():
        if value is not None:
            setattr(article, attribute, value)
    
    db_session.add(article)
    await db_session.commit()
    return article
    