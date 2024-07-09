from .db_api import SessionInstance


async def get_db_session():
    async with SessionInstance() as session:
        yield session