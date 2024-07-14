from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
import sqlalchemy as sa
from sqlalchemy.exc import OperationalError

import asyncio

from my_blog.settings import settings


engine = create_async_engine(settings.get_db_url())

SessionInstance = async_sessionmaker(bind=engine, expire_on_commit=False)


async def test_conn() -> None:
    async with engine.begin() as conn:
        try:
            await conn.execute(sa.text('SELECT 1'))
        except OperationalError:
            print('Conn error')
            return
    print('Conn success')
    return


if __name__ == '__main__':
    asyncio.run(test_conn())