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


def test_ping():
    response = client.get("/api/v1/ping")
    assert response.status_code == 200


async def test_create_article(with_db):
    # Correct request
    response = client.post(
        "/api/v1/articles",
        json={
            "title": "test_create_article_title",
            "content": "test_create_article_content",
            "tags": []
        },
    )
    article = response.json()
    assert response.status_code == 200
    assert all(
        [
            isinstance(article.get("id"), str),
            article.get("title") == "test_create_article_title",
            article.get("content") == "test_create_article_content",
            isinstance(article.get("created_at"), str),
        ]
    )


def test_get_article(with_db):
    # Existing record
    response = client.get("/api/v1/articles/test_article_1")
    article = response.json()
    assert response.status_code == 200
    assert all(
        [
            article.get("id") == "test_article_1",
            article.get("title") == "test_title_1",
            article.get("content") == "test_content_1",
            isinstance(article.get("created_at"), str),
        ]
    )

    # Non-existing record
    response = client.get("/api/v1/articles/fake_id")
    assert response.status_code == 404


def test_get_articles(with_db):
    response = client.get("/api/v1/articles")
    articles = response.json()
    assert response.status_code == 200
    assert len(articles) == 3
    for article in articles:
        assert all(
            [
                isinstance(article.get("id"), str),
                isinstance(article.get("title"), str),
                isinstance(article.get("content"), str),
                isinstance(article.get("created_at"), str),
                article.get('tags') == []
            ]
        )


def test_delete_article(with_db):
    # Exisiting record
    response = client.delete("/api/v1/articles/test_article_1")
    assert response.status_code == 200

    # Non-existing record
    response = client.delete("/api/v1/articles/fake_id")
    assert response.status_code == 200


def test_update_article(with_db):
    response = client.put("/api/v1/articles/test_article_1", json={
        'content': 'test_change_content'
    })
    article = response.json()
    assert response.status_code == 200
    assert all(
        [
            article.get("id") == "test_article_1",
            article.get("title") == "test_title_1",
            article.get("content") == "test_change_content",
            isinstance(article.get("created_at"), str),
            article.get('tags') == []
        ]
    )
