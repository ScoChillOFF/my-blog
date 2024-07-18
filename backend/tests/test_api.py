from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
import pytest
from fastapi.testclient import TestClient

from my_blog.settings import settings
from my_blog.db_api import models
from my_blog import app
from my_blog.dependencies import get_db_session
from . import data as test_data


engine = create_async_engine(settings.get_test_db_url())

TestingSessionInstance = async_sessionmaker(engine, expire_on_commit=False)


@pytest.fixture
async def get_db_and_data() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.drop_all)
        await conn.run_sync(models.Base.metadata.create_all)
    async with TestingSessionInstance() as session:
        res_data = await test_data.get_data_for_tests(session)
    return res_data


async def override_get_db_session():
    async with TestingSessionInstance() as session:
        yield session


app.dependency_overrides[get_db_session] = override_get_db_session

client = TestClient(app)


def test_ping():
    response = client.get("/api/v1/ping")
    assert response.status_code == 200


async def test_create_article(get_db_and_data):
    # Correct request
    response = client.post(
        "/api/v1/articles",
        json={
            "title": "test_create_article_title",
            "content": "test_create_article_content",
            "tags": [],
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


def test_get_article(get_db_and_data):
    # Existing record
    response = client.get("/api/v1/articles/test_article_1")
    article = response.json()
    data = get_db_and_data
    assert response.status_code == 200
    assert article == data["articles"][0]

    # Non-existing record
    response = client.get("/api/v1/articles/fake_id")
    assert response.status_code == 404


def test_get_articles(get_db_and_data):
    data = get_db_and_data

    # All articles
    response = client.get("/api/v1/articles")
    articles = response.json()
    assert response.status_code == 200
    assert articles == data["articles"]

    # By date
    response = client.get("/api/v1/articles?days_limit=0")
    articles = response.json()
    assert response.status_code == 200
    assert articles == data["articles"][0:1]

    response = client.get("/api/v1/articles?days_limit=-1")
    articles = response.json()
    assert response.status_code == 200
    assert articles == []

    response = client.get("/api/v1/articles?days_limit=7")
    articles = response.json()
    assert response.status_code == 200
    assert articles == data["articles"]

    # By single tag
    response = client.get("/api/v1/articles?tags=tag_name_1")
    articles = response.json()
    assert articles == data["articles"][1:]

    # By multiple tags
    response = client.get("/api/v1/articles?tags=tag_name_1&tags=tag_name_2")
    articles = response.json()
    assert articles == data["articles"][1:]


def test_delete_article(get_db_and_data):
    # Exisiting record
    response = client.delete("/api/v1/articles/test_article_1")
    assert response.status_code == 200

    # Non-existing record
    response = client.delete("/api/v1/articles/fake_id")
    assert response.status_code == 200


def test_update_article(get_db_and_data):
    response = client.put(
        "/api/v1/articles/test_article_1", json={"content": "test_change_content"}
    )
    article = response.json()
    valid_article = get_db_and_data["articles"][0]
    valid_article["content"] = "test_change_content"
    assert response.status_code == 200
    assert article == valid_article


def test_get_tags(get_db_and_data):
    data = get_db_and_data
    response = client.get("/api/v1/tags")
    tags = response.json()
    assert response.status_code == 200
    assert tags == data["tags"]
