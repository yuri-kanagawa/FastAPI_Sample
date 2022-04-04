from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_URL = "mysql://user:password@db:3306/sample_db?charset=utf8"

engine = create_engine(DB_URL, echo=True)
#Sqlite を使用するときは connect=_args{'check_same_thread':False}

session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()
# scoped_session
# https://qiita.com/tosizo/items/86d3c60a4bb70eb1656e