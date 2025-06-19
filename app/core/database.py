# from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
# from sqlalchemy.orm import declarative_base
# from typing import AsyncGenerator
#
# from app.core import config
#
# SQLALCHEMY_DATABASE_URL = config.SQLALCHEMY_DATABASE_URL
#
# engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
#
# async_session = async_sessionmaker(
#     bind=engine,
#     expire_on_commit=False,
#     class_=AsyncSession
# )
#
# Base = declarative_base()
#
#
# async def get_db() -> AsyncGenerator[AsyncSession, None]:
#     """
#     Асинхронный генератор сессий базы данных.
#
#     Используется в Depends() FastAPI для получения сессии.
#
#     Yields:
#         AsyncSession: Асинхронная сессия для работы с БД.
#     """
#     async with async_session() as session:
#         yield session


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

from app.core import config

DATABASE_USERNAME = config.DATABASE_USERNAME
DATABASE_PASSWORD = config.DATABASE_PASSWORD
DATABASE_HOST = config.DATABASE_HOST
DATABASE_NAME = config.DATABASE_NAME

SQLALCHEMY_DATABASE_URL = f"postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
