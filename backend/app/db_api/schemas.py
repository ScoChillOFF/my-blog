from pydantic import BaseModel, ConfigDict

from datetime import datetime


class Article(BaseModel):
    title: str
    content: str


class ArticleCreation(Article):
    pass


class ArticleResponse(Article):
    id:str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)