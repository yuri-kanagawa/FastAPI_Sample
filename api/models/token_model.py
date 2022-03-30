from turtle import update
from sqlalchemy import Column, Integer, String, DateTime,ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database_setting import Base
from models.user_model import User

# class Token(Base):
#     __tablename__ = "token"
#     token_id = Column(Integer, primary_key=True,autoincrement=True,nullable='False')
#     user_id = Column(Integer,ForeignKey(User.user_id))
#     access_token = Column(String(100))
#     token_type = Column(String(100))
    