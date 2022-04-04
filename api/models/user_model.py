from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer

from database_setting import Base

class User(Base):
    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True,autoincrement=True,nullable='False')
    name = Column(String(100))
    password = Column(String(100))
    refresh_token = Column(String(200))