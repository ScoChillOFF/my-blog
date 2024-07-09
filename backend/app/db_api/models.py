import sqlalchemy.orm as so

from uuid import uuid4
from datetime import datetime, timezone


class Base(so.DeclarativeBase):
    pass


class Post(Base):
    __tablename__ = 'posts'

    id: so.Mapped[str] = so.mapped_column(primary_key=True, default=lambda: str(uuid4()), index=True)
    title: so.Mapped[str]
    content: so.Mapped[str]
    created_at: so.Mapped[datetime] = so.mapped_column(default=lambda: datetime.now(timezone.utc))