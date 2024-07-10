from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
import pytest
from fastapi.testclient import TestClient

from app.settings import settings
from app.db_api import models
from app import app
from app.dependencies import get_db_session


engine = create_async_engine(settings.get_test_db_url())

TestingSessionInstance = async_sessionmaker(engine, expire_on_commit=False)


@pytest.fixture
async def with_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.drop_all)
        await conn.run_sync(models.Base.metadata.create_all)
    async with TestingSessionInstance() as session:
        session.add_all(
            [
                models.Article(
                    id="test_article_1", title="test_title_1", content="test_content_1"
                ),
                models.Article(
                    id="test_article_2", title="test_title_2", content="test_content_2"
                ),
                models.Article(
                    id="test_article_3", title="test_title_3", content="test_content_3"
                ),
            ]
        )
        await session.commit()


async def override_get_db_session():
    async with TestingSessionInstance() as session:
        yield session


app.dependency_overrides[get_db_session] = override_get_db_session

client = TestClient(app)