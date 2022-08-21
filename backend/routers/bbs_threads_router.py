from typing import Union

from fastapi import APIRouter
from fastapi import Body
from fastapi import Depends
from fastapi import File
from fastapi import Header
from fastapi import status
from fastapi import UploadFile
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from const import error
from const import swagger_tag
from descriptions import bbs_thread_description
from database_setting import get_db
from schemas import bbs_threads_schema
from schemas import success_schema
from stores import bbs_threads_store
from stores import users_store

router = APIRouter()


@router.post(path="/bbs_thread/create/",
                tags=swagger_tag.bbs_thread_tag,
                description=bbs_thread_description.bbs_thread_create,
                status_code=status.HTTP_200_OK,
                response_model=success_schema.ReponseSuccess,
                responses=error.error_response([error.ApiError,
                                                error.Unauthorized,
                                                error.Conflict,
                                                error.Validation]))
def account_create(db:Session=Depends(get_db),
                    token:str=Header(default=...),
                    request_body:bbs_threads_schema.RequestBodyCreateBbs=Body(default=...),
                    image_file: Union[UploadFile,None]=File(default=None)):

    payload_token = users_store.decode_token(token=token)
    users_store.check_token_type(payload_token=payload_token)

    bbs_info = bbs_threads_schema.CreateBbsThread()
    bbs_info.thread_title = request_body.bbs_thread_title
    bbs_info.post_user_name = request_body.post_user_name
    bbs_info.image_file = image_file
    bbs_info.user_id = payload_token["user_id"]

    bbs_threads_store.add_bbs_thread(db=db, value=bbs_info)

    return JSONResponse(content={"status_code": 200})


@router.get(path="/bbs_thread/index/",
                tags=swagger_tag.bbs_thread_tag,
                description=bbs_thread_description.bbs_thread_create,
                status_code=status.HTTP_200_OK,
                response_model=bbs_threads_schema.ResponseReadBbsThreadBase,
                responses=error.error_response([error.ApiError,
                                                error.Unauthorized,
                                                error.Validation]))
def account_create(db:Session=Depends(get_db),
                    token:str=Header(default=...),
                    request_query:bbs_threads_schema.RequestQueryReadBbsThreadBase=Depends()):

    payload_token = users_store.decode_token(token=token)
    users_store.check_token_type(payload_token=payload_token)

    search_info = bbs_threads_schema.SearchGetBbsThread()
    search_info.thread_id = request_query.thread_id
    search_info.like_thread_title = request_query.thread_title
    search_info.post_user_name = request_query.post_user_name
    search_info.is_usage = request_query.is_usage

    bbs_thread_list = bbs_threads_store.get_bbs_thread_list(db=db, value=search_info)

    data_to_json = jsonable_encoder(bbs_thread_list)

    return JSONResponse(content={"status_code": 200, "data": data_to_json})