import shutil

from fastapi import APIRouter
from fastapi import Depends
from fastapi import File
from fastapi import UploadFile
from fastapi import Body
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from database_setting import get_db
from models import user_model
from schemas import login_schema
from database import login_db


router = APIRouter()
tag_name = ['bbs']

@router.post("/create_bbs/", tags=tag_name)
def create_bbs(db: Session = Depends(get_db), upload_file: UploadFile = File(...)):
    print("tet")