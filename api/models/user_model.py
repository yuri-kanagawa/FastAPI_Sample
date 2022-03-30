from turtle import update
from sqlalchemy import Column, Integer, String, DateTime,ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database_setting import Base

class User(Base):
    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True,autoincrement=True,nullable='False')
    name = Column(String(100))
    password = Column(String(100))
    refresh_token = Column(String(100))

    # user_id = Column(Integer, primary_key=True,autoincrement=True,nullable='False')
    # username = Column(String(100))
    # email = Column(String(100))
    # full_name =  Column(String(100))
    # disabled =  Column(String(100))
    # hashed_password = Column(String(100))
