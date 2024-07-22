from copy import deepcopy
from datetime import datetime, timedelta

from my_blog.db_api import models

from sqlalchemy.ext.asyncio import AsyncSession


class Data:
    def __init__(self):
        self.__raw_data: dict[str, list] = get_pre_db_data()
        self.__articles: list[dict] | None = None
        self.__tags: list[dict] | None = None
        self.__prepared_data: dict[str, list] | None = None

    async def fill_db(self, session: AsyncSession) -> None:
        db_data = self.__get_models_from_data()
        session.add_all(db_data)
        await session.commit()

    def __get_models_from_data(self) -> list[models.Base]:
        articles = [
            models.Article(**article_data)
            for article_data in self.__raw_data["articles"]
        ]
        tags = [models.Tag(**tag_data) for tag_data in self.__raw_data["tags"]]
        articles[1].tags = [tags[0]]
        articles[2].tags = [tags[0], tags[1]]
        result = articles + tags
        return result

    def get_data_for_tests(self) -> dict[str, list]:
        if not self.__is_data_prepared():
            self.__prepare_data_for_tests()
        return self.__prepared_data

    def __is_data_prepared(self) -> bool:
        return self.__prepared_data is not None

    def __prepare_data_for_tests(self) -> None:
        self.__prepare_articles_for_tests()
        self.__prepare_tags_for_tests()
        self.__append_relationships_to_test_data()
        self.__prepared_data = {
            "articles": self.__articles,
            "tags": self.__tags
        }

    def __prepare_articles_for_tests(self) -> None:
        self.__articles = deepcopy(self.__raw_data["articles"])
        self.__change_articles_datetime_to_str()

    def __change_articles_datetime_to_str(self) -> None:
        for article in self.__articles:
            article["created_at"] = article["created_at"].isoformat()

    def __prepare_tags_for_tests(self) -> None:
        self.__tags = deepcopy(self.__raw_data["tags"])

    def __append_relationships_to_test_data(self) -> None:
        articles_for_relationships = deepcopy(self.__articles)
        tags_for_relationships = deepcopy(self.__tags)
        self.__articles[0]["tags"] = []
        self.__articles[1]["tags"] = [tags_for_relationships[0]]
        self.__articles[2]["tags"] = [tags_for_relationships[0], tags_for_relationships[1]]
        self.__tags[0]["articles"] = [articles_for_relationships[1], articles_for_relationships[2]]
        self.__tags[1]["articles"] = [articles_for_relationships[2]]


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
    return {
        "articles": sorted(articles_data, key=lambda x: x["created_at"], reverse=True),
        "tags": tags_data,
    }
