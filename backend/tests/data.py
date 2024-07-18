from copy import deepcopy
from datetime import datetime, timedelta

from my_blog.db_api import models


def get_pre_db_data() -> dict[str, list]:
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
    return {"articles": sorted(articles_data, key=lambda x: x["created_at"], reverse=True), "tags": tags_data}


async def fill_db(data, session) -> None:
    articles = [models.Article(**article_data) for article_data in data["articles"]]
    tags = [models.Tag(**tag_data) for tag_data in data["tags"]]
    articles[1].tags = [tags[0]]
    articles[2].tags = [tags[0], tags[1]]
    session.add_all([*articles, *tags])
    await session.commit()


async def get_data_for_tests(session) -> None:
    data = get_pre_db_data()
    await fill_db(data, session)
    prepare_data_for_tests(data)
    return data


def prepare_data_for_tests(data) -> None:
    articles = data["articles"]
    tags = data["tags"]
    for article in articles:
        article["created_at"] = article["created_at"].isoformat()
    rel_articles = deepcopy(data["articles"])
    rel_tags = deepcopy(data["tags"])
    articles[0]["tags"] = []
    articles[1]["tags"] = [rel_tags[0]]
    articles[2]["tags"] = [rel_tags[0], rel_tags[1]]
    tags[0]["articles"] = [rel_articles[1], rel_articles[2]]
    tags[1]["articles"] = [rel_articles[2]]
