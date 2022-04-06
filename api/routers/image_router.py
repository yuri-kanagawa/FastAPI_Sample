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

@router.post("/uploadfile/")
def upload_file(upload_file: UploadFile = File(...)):
    path = f'files/{upload_file.filename}'
    with open(path, 'w+b') as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    return {
        'filename': path,
        'type': upload_file.content_type
    }

@router.get('/download/{name}', response_class=FileResponse)
def get_file(name: str):
    path = f'files/{name}'
    print(type(path))
    return path