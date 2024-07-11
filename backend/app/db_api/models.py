import sqlalchemy.orm as so
import sqlalchemy as sa

from uuid import uuid4
import datetime


class Base(so.DeclarativeBase):
    pass


class Article(Base):
    __tablename__ = 'articles'

    id: so.Mapped[str] = so.mapped_column(primary_key=True, default=lambda: str(uuid4()), index=True)
    title: so.Mapped[str]
    content: so.Mapped[str]
    created_at: so.Mapped[datetime.datetime] = so.mapped_column(sa.DateTime(timezone=True), default=lambda: datetime.datetime.now(datetime.UTC))


class Tag(Base):
    __tablename__ = 'tags'

    id: so.Mapped[str] = so.mapped_column(primary_key=True, default=lambda: str(uuid4()), index=True)
    name: so.Mapped[str] = so.mapped_column(unique=True, index=True)