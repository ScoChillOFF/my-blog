from pydantic import BaseModel, ConfigDict

from datetime import datetime


class ArticleBase(BaseModel):
    title: str
    content: str


class ArticleCreation(ArticleBase):
    pass


class ArticleResponse(ArticleBase):
    id:str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ArticleUpdating(ArticleBase):
    title: str | None = None
    content: str | None = None