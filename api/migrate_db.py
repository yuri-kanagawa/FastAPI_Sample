from sqlalchemy import create_engine

from database_setting import Base

DB_URL = "mysql+pymysql://user:password@db:3306/sample_db?charset=utf8"
engine = create_engine(DB_URL, echo=True)


def reset_database():
    Base.metadata.drop_all(bind=engine)
    
if __name__ == "__main__":
    reset_database()