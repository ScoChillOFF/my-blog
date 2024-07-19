from typing import Iterable

from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa

from datetime import datetime, timezone, timedelta

from . import schemas, models


async def get_tags(db_session: AsyncSession) -> list[models.Tag]:
    query = sa.select(models.Tag)
    result = await db_session.scalars(query)
    tags = result.all()
    for tag in tags:
        tag.articles = sorted(tag.articles, key=lambda x: x.created_at, reverse=True)
    return tags


async def create_article(article_schema: schemas.ArticleCreation, db_session: AsyncSession) -> models.Article:
    article = models.Article(title=article_schema.title, content=article_schema.content)
    await add_tags_to_article(article, article_schema.tags, db_session)
    db_session.add(article)
    await db_session.commit()
    await db_session.refresh(article)
    return article


async def add_tags_to_article(article: models.Article, tag_names: list[str], db_session: AsyncSession) -> None:
    tag_names = [name.lower() for name in tag_names]
    existing_tags = await get_tags_by_names(db_session, tag_names)
    non_existing_tags = await create_non_existing_tags(tag_names, existing_tags, db_session)
    all_tags = existing_tags + non_existing_tags
    article.tags = all_tags


async def create_non_existing_tags(
        tag_names: list[str],
        existing_tags: list[models.Tag],
        db_session: AsyncSession
) -> list[models.Tag]:
    non_existing_tag_names = set(tag_names) - set([tag.name for tag in existing_tags])
    tags = []
    for name in non_existing_tag_names:
        tag = models.Tag(name=name)
        db_session.add(tag)
        tags.append(tag)
    return tags


async def get_tags_by_names(db_session: AsyncSession, tag_names: list[str]) -> list[models.Tag]:
    query = sa.select(models.Tag).where(models.Tag.name.in_(tag_names))
    tags = (await db_session.scalars(query)).all()
    return tags


async def get_article(article_id: str, db_session: AsyncSession) -> models.Article:
    article = await db_session.get(models.Article, article_id)
    return article


async def get_articles(db_session: AsyncSession, days_limit: int | None = None, tag_names: list[str] | None = None) -> \
list[models.Article]:
    query = sa.select(models.Article).order_by(models.Article.created_at.desc())
    if days_limit is not None:
        query = apply_days_limit(query, days_limit)
    if tag_names is not None:
        query = apply_tags_filter(query, tag_names)
    result = await db_session.scalars(query)
    articles = result.all()
    return articles


def apply_tags_filter(query: sa.Select, tag_names: list[str]) -> sa.Select:
    query = query.join(models.Article.tags).filter(models.Tag.name.in_(tag_names)).distinct()
    return query


def apply_days_limit(query: sa.Select, days_limit: int) -> sa.Select:
    converted_days = timedelta(days=days_limit)
    current_date = datetime.now(tz=timezone.utc).astimezone().date()
    return query.where(models.Article.created_at >= current_date - converted_days)


async def delete_article(article_id: str, db_session: AsyncSession) -> None:
    article = await get_article(article_id=article_id, db_session=db_session)
    if not article:
        return
    await db_session.delete(article)
    await db_session.commit()
    return


async def update_article(article_id: str, article_schema: schemas.ArticleUpdating,
                         db_session: AsyncSession) -> models.Article | None:
    article = await get_article(article_id=article_id, db_session=db_session)
    if not article:
        return

    for attribute, value in article_schema.model_dump().items():
        if value is not None:
            setattr(article, attribute, value)

    db_session.add(article)
    await db_session.commit()
    return article
