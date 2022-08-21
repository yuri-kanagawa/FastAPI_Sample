import os
import shutil
import sys
from datetime import datetime
from typing import List


from fastapi import HTTPException
from pytz import timezone
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import case

from const import error
from const import error_message
from const import flag_value
from const import initial_value
from log_setting import Log
from schemas import bbs_threads_schema
from models import bbs_threads_model
from models import users_model


"""
掲示板スレッド作成
"""
def add_bbs_thread(db:Session,
                    value:bbs_threads_schema.CreateBbsThread):

    now_datetime = datetime.now(timezone("Asia/Tokyo"))

    search_info = bbs_threads_schema.SearchGetBbsThread()
    search_info.strict_thread_title = value.thread_title

    exist_bbs_thread = get_bbs_thread_list(db=db, value=search_info)

    if len(exist_bbs_thread) > 0:
        file_name = "file: " +  __file__
        method_name = "method: " + sys._getframe().f_code.co_name
        error_contant = error_message.already_existed + " BbsThread"
        message = file_name + " " + method_name + " " + error_contant

        log=Log()
        log.error_log(message)

        raise HTTPException(status_code=error.InternalServer.status_code,
                            detail={"type": error.InternalServer.detail,
                                    "msg": error_contant})

    try:
        bbs_thread = bbs_threads_model.BbsThreadModel()
        bbs_thread.post_user_id = value.user_id
        bbs_thread.thread_title = value.thread_title
        bbs_thread.post_user_name = value.post_user_name

        if value.image_file:
            
            env_file_directory = os.environ["file_directory"]
            image_save_folder = env_file_directory + "files/"

            if os.path.exists(image_save_folder) == False:
                os.makedirs(name=image_save_folder, mode=0o777, exist_ok=True)
            
            
            file_extension = os.path.basename(value.image_file.filename).split('.', 1)[1]
            value.image_file.filename = f"{value.thread_title}.{file_extension}"
            post_image_file_name = value.image_file.filename
            save_path = f"{image_save_folder}{post_image_file_name}"
            with open(save_path, 'w+b') as buffer:
                shutil.copyfileobj(value.image_file.file, buffer)
            bbs_thread.image_path = save_path

        else:
            bbs_thread.image_path = ""

        bbs_thread.is_usage = initial_value.is_usage
        bbs_thread.create_at = now_datetime
        bbs_thread.update_at = now_datetime

        db.add(bbs_thread)
        db.flush()
    except:
        db.rollback()
        file_name = "file: " +  __file__
        method_name = "method: " + sys._getframe().f_code.co_name
        error_contant = error_message.create_error + " BbsThread"
        message = file_name + " " + method_name + " " + error_contant

        log=Log()
        log.error_log(message)

        raise HTTPException(status_code=error.InternalServer.status_code,
                            detail={"type": error.InternalServer.detail,
                                    "msg": error_contant})


    db.commit()


"""
掲示板一覧取得
"""
def get_bbs_thread_list(db:Session,
                        value:bbs_threads_schema.SearchGetBbsThread)\
        -> List[bbs_threads_model.BbsThreadModel]:

    bbs_threads_table = bbs_threads_model.BbsThreadModel
    users_table = users_model.UsersModel

    filter_conditions_list = []

    if value.thread_id:
        filter_conditions_list.append(bbs_threads_table.id == value.thread_id)

    if value.like_thread_title:
        filter_conditions_list.append(bbs_threads_table.thread_title.like("%" + value.like_thread_title + "%"))

    if value.strict_thread_title:
        filter_conditions_list.append(bbs_threads_table.thread_title == value.strict_thread_title)

    if value.post_user_name:
        filter_conditions_list.append(bbs_threads_table.post_user_name.like("%" + value.post_user_name + "%"))

    if value.is_usage:
        filter_conditions_list.append(bbs_threads_table.is_usage == flag_value.is_usage)

    thread_list = db.query(bbs_threads_table).\
                    join(users_table,
                            users_table.id == bbs_threads_table.post_user_id).\
                    filter(*filter_conditions_list).\
                    order_by(bbs_threads_table.id).\
                    with_entities(
                        bbs_threads_table.id.label("thread_id"),
                        bbs_threads_table.thread_title.label("bbs_thread_title"),
                        bbs_threads_table.image_path.label("image_path"),
                        bbs_threads_table.post_user_name.label("create_thread_user_name"),
                        users_table.name.label("account_user_name"),
                        case([(bbs_threads_table.is_usage == flag_value.is_usage, True)],else_=False).label("bbs_thread_is_usage"),
                    ).\
                    all()

    return thread_list