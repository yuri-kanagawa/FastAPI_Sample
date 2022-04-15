import datetime
import shutil
from typing import List
from typing import Tuple

from fastapi import UploadFile
from sqlalchemy import func
from sqlalchemy import desc
from sqlalchemy.orm import Session

from models import bbs_thread_model
from schemas import bbs_thread_schema


def create_thread(db: Session, bbs_thread: bbs_thread_schema.ThreadBase ,upload_file: UploadFile) -> bbs_thread_model.BbsThread:
    bbs_create_time = datetime.datetime.now()

    if(upload_file == None):
        db_bbs =  bbs_thread_model.BbsThread(
            thread_title = bbs_thread.thread_title,
            anime_id = bbs_thread.anime_id,
            tag = bbs_thread.tag,
            # image = bbs_thread.image,
            user_id = bbs_thread.user_id,
            ipaddress = bbs_thread.ipaddress,
            create_at = bbs_create_time,
            update_at = bbs_create_time)
        db.add(db_bbs)
        db.commit()
        db.refresh(db_bbs)
        return db_bbs.thread_title
    
    #画像を送信された場合の処理
    else:
        image_file_name = bbs_thread.thread_title + '_0_title'
        file_split = upload_file.filename.split('.')
        path = f'files/{image_file_name}.{file_split[1]}'

        with open(path, 'w+b') as buffer:
            shutil.copyfileobj(upload_file.file, buffer)

        db_bbs =  bbs_thread_model.BbsThread(
            thread_title = bbs_thread.thread_title,
            anime_id = bbs_thread.anime_id,
            tag = bbs_thread.tag,
            image = image_file_name,
            user_id = bbs_thread.user_id,
            ipaddress = bbs_thread.ipaddress,
            create_at = bbs_create_time,
            update_at = bbs_create_time)
        db.add(db_bbs)
        db.commit()
        db.refresh(db_bbs)
        return db_bbs.thread_title
