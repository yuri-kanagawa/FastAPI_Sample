from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy.dialects.mysql import TINYINT

from database_setting import Base
from models import users_model

class BbsThreadModel(Base):
    __tablename__ = "t_bbs_thread"

    user_table = users_model.UsersModel

    id = Column(Integer, primary_key=True, autoincrement=True, nullable='False')
    thread_title = Column(String(20), nullable='False', unique=True)
    post_user_id = Column(Integer, ForeignKey(user_table.id),nullable='False')
    post_user_name = Column(String(20), nullable='False')
    image_path = Column(String(255), nullable='False')
    is_usage = Column(TINYINT, nullable='False')
    create_at = Column(DateTime, nullable='False')
    update_at = Column(DateTime, nullable='False')