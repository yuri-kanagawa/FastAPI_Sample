from sqlalchemy import Column
from sqlalchemy import DATETIME
from sqlalchemy import Integer
from sqlalchemy import String

from database_setting import Base

class AnimeList(Base):
    __tablename__ = "anime_list"

    anime_id = Column(Integer,primary_key=True,nullable='False')
    anime_title = Column(String(100),nullable='False',unique=True)
    subsc_id_list = Column(String(100))
    genre_id_list = Column(String(100))
    start_at = Column(DATETIME, nullable=False)
    end_at = Column(DATETIME, nullable=False)