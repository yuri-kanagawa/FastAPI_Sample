from sqlalchemy import create_engine

#元はDB.py のインスタンスを使用
from models.task import Base
# from models.anime_vote_model import AnimeVoteBase

DB_URL = "mysql+pymysql://user:password@db:3306/sample_db?charset=utf8"
engine = create_engine(DB_URL, echo=True)


def reset_database():
    Base.metadata.drop_all(bind=engine)
    # Base.metadata.create_all(bind=engine)
    # taskモデルベースでDB作成
    # TaskBase.metadata.drop_all(bind=engine)
    # TaskBase.metadata.create_all(bind=engine)
    # #animevotebase モデル
    # AnimeVoteBase.metadata.drop_all(bind=engine)
    # AnimeVoteBase.metadata.create_all(bind=engine)

if __name__ == "__main__":
    reset_database()