from enum import unique
from sqlalchemy import Column, Integer, String, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime

from database_setting import Base

#sqlalchemy を利用してDB作成

class AnimeList(Base):
    __tablename__ = "anime_list"

    anime_id = Column(Integer,primary_key=True,nullable='False')
    anime_title = Column(String(100),nullable='False',unique=True)
    subsc_id_list = Column(String(100))
    genre_id_list = Column(String(100))
    start_at = Column(DATETIME, nullable=False)
    end_at = Column(DATETIME, nullable=False)