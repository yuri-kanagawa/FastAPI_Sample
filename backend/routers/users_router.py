import sys

from fastapi import APIRouter
from fastapi import Body
from fastapi import Depends
from fastapi import Header
from fastapi import HTTPException
from fastapi import status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from const import error_message
from const import error
from const import swagger_tag
from descriptions import users_description
from database_setting import get_db
from log_setting import Log
from schemas import users_schema
from schemas import success_schema
from stores import users_store

router = APIRouter()


@router.post(path="/user/create/",
                tags=swagger_tag.user_tag,
                description=users_description.user_create,
                status_code=status.HTTP_200_OK,
                response_model=success_schema.ReponseSuccess,
                responses=error.error_response([error.ApiError,
                                                error.Unauthorized,
                                                error.Conflict,
                                                error.Validation]))
def account_create(db:Session=Depends(get_db),
                    request_body:users_schema.RequestBodyCreateUserBase=Body(default=...)):

    registar_info = users_schema.SearchUserSearch()
    registar_info.user_name = request_body.user_name

    exist_user = users_store.get_prefix_user(db=db, value=registar_info)

    if exist_user:
        raise HTTPException(status_code=error.Conflict.status_code,
                            detail={"type": error.Conflict.detail,
                                    "msg": error_message.already_existed + " User"})


    users_store.add_user(db=db, value=request_body)
    return JSONResponse(content={"status_code": 200})


@router.post(path="/user/login/",
                tags=swagger_tag.user_tag,
                description=users_description.user_login,
                status_code=status.HTTP_200_OK,
                response_model=users_schema.ResponseBodyLoginBase,
                responses=error.error_response([error.ApiError,
                                                error.Validation]))
def login(db:Session=Depends(get_db),
            request_body:users_schema.RequestBodyLoginUserBase=Body(default=...)):

    login_info = users_schema.SearchUserSearch()
    login_info.user_name = request_body.user_name
    user = users_store.get_prefix_user(db=db, value=login_info)

    users_store.check_user_password(plain_password=request_body.password,
                                    user_password=user.password)

    access_token = users_store.create_access_tokens(user_id=user.id)
    refresh_token = users_store.create_refresh_token(db=db, user=user)

    reponse_dict = {}
    reponse_dict["user_id"] = user.id
    reponse_dict["user_name"] = user.name
    reponse_dict["access_token"] = access_token
    reponse_dict["refresh_token"] = refresh_token

    log = Log()
    message = f"userid: {user.id} user_name: {user.name} LgoIn Success"
    log.user_login_log(message)

    return JSONResponse(content={"status_code": 200, "data":reponse_dict})


@router.post(path="/user/login/token/",
                tags=swagger_tag.user_tag,
                description=users_description.user_login_token,
                status_code=status.HTTP_200_OK,
                response_model=users_schema.ResponseTokenBase,
                responses=error.error_response([error.ApiError,
                                                error.Unauthorized,
                                                error.Validation]))
def user_login_token(db:Session=Depends(get_db),
                        token:str=Header(default=...)):

    payload_token = users_store.decode_token(token=token)
    users_store.check_token_type(payload_token=payload_token)

    token_dict = {}
    if payload_token['token_type'] == "access_token":
        token_dict["access_token"] = users_store.create_access_tokens(payload_token["user_id"])
    
    elif payload_token["token_type"] == "refresh_token":
        search_info = users_schema.SearchUserSearch()
        search_info.user_id = payload_token["user_id"]
        search_info.refresh_token = token
        token_dict["refresh_token"] = users_store.check_refresh_token(db=db,value=search_info)


    return JSONResponse(content={"status_code": 200, "data":token_dict})



@router.post(path="/user/logout/",
                tags=swagger_tag.user_tag,
                description=users_description.user_logout,
                status_code=status.HTTP_200_OK,
                response_model=success_schema.ReponseSuccess,
                responses=error.error_response([error.ApiError,
                                                error.Validation]))
def logout(db:Session=Depends(get_db),
            token:str=Header(default=...)):

    payload_token = users_store.decode_token(token=token)
    login_info = users_schema.SearchUserSearch()
    login_info.user_id = payload_token["user_id"]
    user = users_store.get_prefix_user(db=db, value=login_info)
    users_store.empty_refresh_token(db=db, user=user)

    log = Log()
    message = f"userid: {user.id} user_name: {user.name} LogOut Success"
    log.user_login_log(message)

    return JSONResponse(content={"status_code": 200})


@router.get(path="/user/index/",
                tags=swagger_tag.user_tag,
                summary="Get Available All User",
                description=users_description.user_index,
                status_code=status.HTTP_200_OK,
                response_model=users_schema.ReponseReadUserBase,
                responses=error.error_response([error.ApiError,
                                                error.Validation]))
def read_user_list(db:Session=Depends(get_db),
                    token:str=Header(default=...),
                    request_query:users_schema.RequestQueryReadUserBase=Depends()):

    payload_token = users_store.decode_token(token=token)
    users_store.check_token_type(payload_token=payload_token)

    user_list = users_store.get_all_users(db=db, value=request_query)

    data_to_json = jsonable_encoder(user_list)

    return JSONResponse(content={"status_code": 200, "data": data_to_json})


@router.put(path="/user/update/",
                tags=swagger_tag.user_tag,
                description=users_description.user_update,
                status_code=status.HTTP_200_OK,
                response_model=success_schema.ReponseSuccess,
                responses=error.error_response([error.ApiError,
                                                error.Validation]))
def user_update(db:Session=Depends(get_db),
                token:str=Header(default=...),
                request_body:users_schema.RequestBodyUpdateUserInfo=Body(default=None)):
    
    if len(request_body.user_name) == 0\
            and len(request_body.password) == 0:

        file_name = "file: " +  __file__
        method_name = "method: " + sys._getframe().f_code.co_name
        error_contant = error_message.not_exist_value + " username or password"
        message = file_name + " " + method_name + " " + error_contant

        log=Log()
        log.error_log(message)
        raise HTTPException(status_code=error.ApiError.status_code,
                            detail={"type": error.ApiError.detail,
                                    "msg": error_contant})

    payload_token = users_store.decode_token(token=token)
    update_info = users_schema.UpdateUserInfo()
    update_info.user_id = payload_token["user_id"]
    update_info.user_name = request_body.user_name
    update_info.password = request_body.password

    users_store.edit_user(db=db, value=update_info)

    return JSONResponse(content={"status_code": 200})


@router.put(path="/user/update/usage/",
                tags=swagger_tag.user_tag,
                description=users_description.user_update_usage,
                status_code=status.HTTP_200_OK,
                response_model=success_schema.ReponseSuccess,
                responses=error.error_response([error.ApiError,
                                                error.Validation]))
def user_update(db:Session=Depends(get_db),
                token:str=Header(default=...)):


    payload_token = users_store.decode_token(token=token)

    update_info = users_schema.UpdateUserInfo()
    update_info.user_id = payload_token["user_id"]
    update_info.is_usage = True
    users_store.edit_user(db=db, value=update_info)

    return JSONResponse(content={"status_code": 200})