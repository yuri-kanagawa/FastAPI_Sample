# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
# from sqlalchemy.orm import sessionmaker, declarative_base
# import asyncio
# import aiomysql
# from api.models.anime_vote_model import AnimeVote

# ASYNC_DB_URL = "mysql+aiomysql://user:password@db:3306/sample_db?charset=utf8"

# async_engine = create_async_engine(ASYNC_DB_URL, echo=True)
# async_session = sessionmaker(
#     autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession
# )

# async def get_db():
#     async with async_session() as session:
#         yield session


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_URL = "mysql://user:password@db:3306/sample_db?charset=utf8"

engine = create_engine(DB_URL, echo=True)
#Sqlite を使用するときは connect=_args{'check_same_thread':False}

session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
# TaskBase = declarative_base()
# AnimeVoteBase = declarative_base()

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()
# scoped_session
# https://qiita.com/tosizo/items/86d3c60a4bb70eb1656e