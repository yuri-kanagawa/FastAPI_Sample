from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy.dialects.mysql import TINYINT

from database_setting import Base

class UsersModel(Base):
    __tablename__ = "t_user"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable='False')
    name = Column(String(20), nullable='False', unique=True)
    password = Column(String(60), nullable='False')
    refresh_token = Column(String(255), nullable='False')
    is_usage = Column(TINYINT, nullable='False')
    create_at = Column(DateTime, nullable='False')
    update_at = Column(DateTime, nullable='False')