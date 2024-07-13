from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
import pytest
from fastapi.testclient import TestClient

from datetime import datetime, timedelta, timezone

from app.settings import settings
from app.db_api import models
from app import app
from app.dependencies import get_db_session


engine = create_async_engine(settings.get_test_db_url())

TestingSessionInstance = async_sessionmaker(engine, expire_on_commit=False)


@pytest.fixture
async def get_db_and_data(get_pre_db_data) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.drop_all)
        await conn.run_sync(models.Base.metadata.create_all)
    async with TestingSessionInstance() as session:
        data = get_pre_db_data
        articles = [models.Article(**article_data) for article_data in data["articles"]]
        tags = [models.Tag(**tag_data) for tag_data in data["tags"]]
        articles[1].tags = [tags[0]]
        articles[2].tags = [tags[0], tags[1]]
        session.add_all([*articles, *tags])
        await session.commit()

    articles_data = data["articles"]
    tags_data = data["tags"]
    articles_data[0]["tags"] = []
    articles_data[1]["tags"] = [tags_data[0]]
    articles_data[2]["tags"] = [tags_data[0], tags_data[1]]
    for article in articles_data:
        article["created_at"] = (
            article["created_at"].isoformat().replace("+00:00", "+03:00")
        )
    return data


@pytest.fixture
def get_pre_db_data() -> dict[str, str]:
    articles_data = [
        {
            "id": "test_article_1",
            "title": "test_title_1",
            "content": "test_content_1",
            "created_at": datetime.now().astimezone(),
        },
        {
            "id": "test_article_2",
            "title": "test_title_2",
            "content": "test_content_2",
            "created_at": datetime.now().astimezone() - timedelta(days=1),
        },
        {
            "id": "test_article_3",
            "title": "test_title_3",
            "content": "test_content_3",
            "created_at": datetime.now().astimezone() - timedelta(days=7),
        },
    ]
    tags_data = [
        {"id": "test_tag_1", "name": "tag_name_1"},
        {"id": "test_tag_2", "name": "tag_name_2"},
    ]
    return {"articles": articles_data, "tags": tags_data}


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

    # TODO: ////////////////////////////// tests for days limit ///////////////////////
    #
    # /////////////////////////////////////////////////////////////////////////////////

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
