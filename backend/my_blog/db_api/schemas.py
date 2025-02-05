from pydantic import BaseModel, ConfigDict

from datetime import datetime


class TagSubResponse(BaseModel):
    id: str
    name: str


class TagResponse(BaseModel):
    id: str
    name: str
    articles: list['ArticleSubResponse']


class ArticleCreation(BaseModel):
    title: str
    content: str
    tags: list[str] | None


class ArticleResponse(BaseModel):
    id: str
    title: str
    content: str
    created_at: datetime
    tags: list[TagSubResponse]

    model_config = ConfigDict(from_attributes=True)


class ArticleSubResponse(BaseModel):
    id: str
    title: str
    content: str
    created_at: datetime


class ArticleUpdating(BaseModel):
    title: str | None = None
    content: str | None = None