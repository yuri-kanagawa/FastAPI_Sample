from turtle import update
from sqlalchemy import Column, Integer, String, DateTime,ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from database_setting import Base
from models.anime_list_model import AnimeList
#sqlalchemy を利用してDB作成
#
class AnimeVote(Base):
    __tablename__ = "anime_vote"

    vote_id = Column(Integer, primary_key=True,autoincrement=True,nullable='False')
    anime_id = Column(Integer,ForeignKey(AnimeList.anime_id))
    # ondelete='SET NULL' は参照元が消えたときにNull
    # anime_id = Column(Integer,ForeignKey(AnimeList.anime_id))
    user_id = Column(String(100))
    ipaddress = Column(String(100))
    create_at = Column(DateTime, nullable=False)
    update_at = Column(DateTime, nullable=False)

#ForeignKey
#外部キーの指定
#ondelete をつけると親のデータが消えた場合にセットすることができる

#relationship とは
#SQL の Join を行うもの
#参考記事 : https://www.python.ambitious-engineer.com/archives/1579

#relation の引数って何するの？
# 参考記事 : https://qiita.com/1234224576/items/ba66838b32b99cce51d2

