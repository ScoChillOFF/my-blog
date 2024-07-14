import sqlalchemy.orm as so
import sqlalchemy as sa

from uuid import uuid4
import datetime


class Base(so.DeclarativeBase):
    pass


association_table = sa.Table(
    "tags_articles",
    Base.metadata,
    sa.Column("tag_id", sa.ForeignKey("tags.id"), primary_key=True),
    sa.Column("article_id", sa.ForeignKey("articles.id"), primary_key=True),
)


class Article(Base):
    __tablename__ = 'articles'

    id: so.Mapped[str] = so.mapped_column(primary_key=True, default=lambda: str(uuid4()), index=True)
    title: so.Mapped[str]
    content: so.Mapped[str]
    created_at: so.Mapped[datetime.datetime] = so.mapped_column(sa.DateTime(timezone=True), default=lambda: datetime.datetime.now(datetime.UTC))

    tags: so.Mapped[list['Tag']] = so.relationship(secondary=association_table, back_populates='articles', lazy='selectin')


class Tag(Base):
    __tablename__ = 'tags'

    id: so.Mapped[str] = so.mapped_column(primary_key=True, default=lambda: str(uuid4()), index=True)
    name: so.Mapped[str] = so.mapped_column(unique=True, index=True)

    articles: so.Mapped[list['Article']] = so.relationship(secondary=association_table, back_populates='tags', lazy='selectin')