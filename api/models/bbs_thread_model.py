from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String

from database_setting import Base
from models.anime_list_model import AnimeList

class BbsThread(Base):
    __tablename__ = "bbs_thread"

    thread_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    thread_title = Column(Integer, unique=True, autoincrement=True, nullable=False)
    anime_id = Column(Integer,ForeignKey(AnimeList.anime_id), nullable=True)
    # ondelete='SET NULL' は参照元が消えたときにNull
    user_id = Column(String(100))
    ipaddress = Column(String(100))
    create_at = Column(DateTime, nullable=False)
    create_at = Column(DateTime, nullable=False)