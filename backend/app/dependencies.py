from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from typing import Annotated

from .db_api import SessionInstance


async def get_db_session():
    async with SessionInstance() as session:
        yield session


DBSession = Annotated[AsyncSession, Depends(get_db_session)]