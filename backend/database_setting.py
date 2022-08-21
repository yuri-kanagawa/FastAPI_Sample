import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#.envファイルの読み出し
load_dotenv()
env_db_name = os.environ["db_name"]
env_db_user = os.environ["db_user"]
env_db_pass = os.environ["db_pass"]
env_db_serv = os.environ["db_serv"]
env_db_port = os.environ["db_port"]

DB_URL = f"mysql://{env_db_user}:{env_db_pass}@{env_db_serv}:{env_db_port}/{env_db_name}?charset=utf8"

engine = create_engine(DB_URL, echo=True)

session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()