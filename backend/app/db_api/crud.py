from sqlalchemy.ext.asyncio import AsyncSession

from . import schemas, models


async def create_article(article_schema: schemas.Article, db_session: AsyncSession) -> models.Article:
    article = models.Article(**article_schema.model_dump())
    db_session.add(article)
    await db_session.commit()
    await db_session.refresh(article)
    return article


async def get_article(article_id: str, db_session: AsyncSession) -> models.Article:
    article = await db_session.get(models.Article, article_id)
    return article