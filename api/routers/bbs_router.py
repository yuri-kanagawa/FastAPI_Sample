import shutil
from typing import Optional

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Form
from fastapi import File
from fastapi import UploadFile
from fastapi import Body
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from database_setting import get_db
from models import bbs_thread_model
from schemas import bbs_thread_schema
from database import bbs_db


router = APIRouter()
tag_name = ['bbs']

@router.post("/create_bbs", tags=tag_name, response_model=bbs_thread_schema.ThreadBase)
def create_bbs(bbs_thread:bbs_thread_schema.ThreadBase =  Depends(bbs_thread_schema.ThreadBase.as_form), upload_file:UploadFile = File(None), db: Session = Depends(get_db)):
# def create_bbs(bbs_thread:bbs_schema.ThreadBase, db: Session = Depends(get_db)):
    print("aa")
    print(bbs_thread.thread_title)
    # data = bbs_db.create_thread(db = db, bbs_thread = bbs_thread ,upload_file = upload_file)
    data = bbs_db.create_thread(db = db, bbs_thread = bbs_thread ,upload_file = upload_file)
    data_to_json = jsonable_encoder(data)
    return JSONResponse(content={'status_code': 200, 'data':data_to_json})