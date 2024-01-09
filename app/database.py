from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel import SQLModel

from app.config import settings


if settings.MODE == 'TEST':
    DATABASE_URL = settings.TEST_DATABASE_URL
    DATABASE_PARAMS = {"poolclass": NullPool, "echo": False}
else:
    DATABASE_URL = settings.DATABASE_URL
    DATABASE_PARAMS = {"echo": settings.SQL_ECHO}


engine = create_async_engine(DATABASE_URL, **DATABASE_PARAMS)
async_session_factory = async_sessionmaker(engine, expire_on_commit=False)


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
