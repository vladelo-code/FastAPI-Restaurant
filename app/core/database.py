from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base

from app.core import config

SQLALCHEMY_DATABASE_URL = config.SQLALCHEMY_DATABASE_URL

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

async_session = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)

Base = declarative_base()


async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session
