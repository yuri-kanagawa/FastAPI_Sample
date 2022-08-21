import sys
from datetime import datetime
from datetime import timedelta
from typing import List

from fastapi import HTTPException
from jose import jwt
from pytz import timezone
from sqlalchemy.orm import Session

from const import error
from const import error_message
from const import flag_value
from const import initial_value
from log_setting import Log
from password_hash import Hash
from schemas import users_schema
from models import users_model

"""
ユーザー作成
"""
def add_user(db:Session, value:users_schema.RequestBodyCreateUserBase):

    now_datetime = datetime.now(timezone("Asia/Tokyo"))

    hash = Hash()
    hashed_password = hash.get_password_hash(value.password)

    try:

        user = users_model.UsersModel()
        user.name = value.user_name
        user.password = hashed_password
        user.is_usage = initial_value.is_usage
        user.refresh_token = ""
        user.create_at = now_datetime
        user.update_at = now_datetime

        db.add(user)
        db.flush()

    except:
        db.rollback()
        file_name = "file: " +  __file__
        method_name = "method: " + sys._getframe().f_code.co_name
        error_contant = error_message.create_error + "User"
        message = file_name + " " + method_name + " " + error_contant

        log=Log()
        log.error_log(message)

        raise HTTPException(status_code=error.InternalServer.status_code,
                            detail={"type": error.InternalServer.detail,
                                    "msg": error_contant})

    db.commit()

"""
特定のユーザー取得
"""
def get_prefix_user(db:Session, value:users_schema.SearchUserSearch)\
        -> users_model.UsersModel:

    users_table = users_model.UsersModel

    filter_conditions_list = []

    if value.user_id:
        filter_conditions_list.append(users_table.id == value.user_id)

    if value.user_name:
        filter_conditions_list.append(users_table.name == value.user_name)

    if value.password:
        filter_conditions_list.append(users_table.password == value.password)

    if value.is_usage == True:
        filter_conditions_list.append(users_table.is_usage == flag_value.is_usage)
    elif value.is_usage == False:
         filter_conditions_list.append(users_table.is_usage == flag_value.not_usage)
    
    if value.refresh_token:
        filter_conditions_list.append(users_table.refresh_token == value.refresh_token)


    prefix_user = db.query(users_table).\
                        filter(*filter_conditions_list).\
                        first()
    
    return prefix_user


"""
全てのユーザーを取得
"""
def get_all_users(db:Session, value:users_schema.RequestQueryReadUserBase)\
        -> List[users_model.UsersModel]:

    users_table = users_model.UsersModel

    filter_conditions_list = []

    if value.user_id:
        filter_conditions_list.append(users_table.id == value.user_id)

    if value.user_name:
        filter_conditions_list.append(users_table.name.like("%" + value.user_name + "%"))

    if value.is_usage == True:
        filter_conditions_list.append(users_table.is_usage == flag_value.is_usage)
    elif value.is_usage == False:
        filter_conditions_list.append(users_table.is_usage == flag_value.not_usage)

    available_usrs = db.query(users_table).\
                        filter(*filter_conditions_list).\
                        order_by(users_table.id).\
                        with_entities(
                            users_table.id.label("user_id"),
                            users_table.name.label("user_name"),
                        ).\
                        all()

    return available_usrs

"""
アクセストークンの作成
"""
def create_access_tokens(user_id:users_model.UsersModel.id)\
        -> dict:

        now_datetime = datetime.now(timezone('Asia/Tokyo'))

        try:
            access_payload = {}
            access_payload["token_type"] = "access_token"
            access_payload["exp"] = now_datetime + timedelta(minutes=60)
            access_payload["user_id"] = user_id

            # 'SECRET_KEY123' should be complicated
            # 'SECRET_KEY123' は複雑にしたほうがいい
            access_token = jwt.encode(access_payload, 'SECRET_KEY123',algorithm='HS256')
            return access_token
        except:

            file_name = "file: " +  __file__
            method_name = "method: " + sys._getframe().f_code.co_name
            error_contant = error_message.update_error + "AccessToken"
            message = file_name + " " + method_name + " " + error_contant

            log=Log()
            log.error_log(message)

            raise HTTPException(status_code=error.InternalServer.status_code,
                                detail={"type": error.InternalServer.detail,
                                        "msg": error_contant})


"""
リフレッシュトークン作成
"""
def create_refresh_token(db:Session, user:users_model.UsersModel)\
        ->str:

    try:

        now_datetime = datetime.now(timezone('Asia/Tokyo'))

        refresh_payload = {}
        refresh_payload["token_type"] = "refresh_token"
        refresh_payload["exp"] = now_datetime + timedelta(days=90)
        refresh_payload["user_id"] = user.id
        # 'SECRET_KEY123' should be complicated
        # 'SECRET_KEY123' は複雑にしたほうがいい
        refresh_token = jwt.encode(refresh_payload, 'SECRET_KEY123', algorithm='HS256')
        user.refresh_token = refresh_token
        db.flush()

    except:
        db.rollback()
        file_name = "file: " +  __file__
        method_name = "method: " + sys._getframe().f_code.co_name
        error_contant = error_message.update_error + "RefreshToken"
        message = file_name + " " + method_name + " " + error_contant

        log=Log()
        log.error_log(message)

        raise HTTPException(status_code=error.InternalServer.status_code,
                            detail={"type": error.InternalServer.detail,
                                    "msg": error_contant})
    
    db.commit()

    return refresh_token


def check_user_password(plain_password:str,
                        user_password:users_model.UsersModel.password):

    hash = Hash()
    check_password = hash.verify_password(hashed_password=user_password,
                                            plain_password=plain_password)

    if check_password == False:
        file_name = "file: " +  __file__
        method_name = "method: " + sys._getframe().f_code.co_name
        error_contant = error_message.unmatch + " Password"
        message = file_name + " " + method_name + " " + error_contant

        log=Log()
        log.error_log(message)
        raise HTTPException(status_code=error.Unauthorized.status_code,
                            detail={"type": error.Unauthorized.detail,
                                    "msg": error_contant})


"""
トークン解読
"""
def decode_token(token:dict) -> dict:

    try:
        decode_result = jwt.decode(token, 'SECRET_KEY123', algorithms=['HS256'])
        return decode_result
    except:
        file_name = "file: " +  __file__
        method_name = "method: " + sys._getframe().f_code.co_name
        error_contant = "Failed Decode Token"
        message = file_name + " " + method_name + " " + error_contant

        log=Log()
        log.error_log(message)
        raise HTTPException(status_code=error.InternalServer.status_code,
                            detail={"type": error.InternalServer.detail,
                                    "msg": error_contant})

"""
tokenタイプチェック
"""
def check_token_type(payload_token:dict):

    if payload_token['token_type'] != "access_token" and\
            payload_token['token_type'] != "refresh_token":

        file_name = "file: " +  __file__
        method_name = "method: " + sys._getframe().f_code.co_name
        error_contant = error_message.unmatch + " TokenType"
        message = file_name + " " + method_name + " " + error_contant

        log=Log()
        log.error_log(message)
        raise HTTPException(status_code=error.Unauthorized.status_code,
                            detail={"type": error.Unauthorized.detail,
                                    "msg": error_contant})

"""
リフレッシュトークンチェック
"""
def check_refresh_token(db:Session, value:users_schema.SearchUserSearch):

    user = get_prefix_user(db=db, value=value)

    if user:
        return create_refresh_token(db=db, user=user)

    else:
        file_name = "file: " +  __file__
        method_name = "method: " + sys._getframe().f_code.co_name
        error_contant = error_message.unmatch + " UserId or RefreshToken"
        message = file_name + " " + method_name + " " + error_contant

        log=Log()
        log.error_log(message)
        raise HTTPException(status_code=error.Unauthorized.status_code,
                            detail={"type": error.Unauthorized.detail,
                                    "msg": error_contant})


def empty_refresh_token(db:Session, user:users_model.UsersModel):

    try:
        user.refresh_token = ""
        db.flush()

    except:
        db.rollback()
        file_name = "file: " +  __file__
        method_name = "method: " + sys._getframe().f_code.co_name
        error_contant = error_message.update_error + " RefreshToken"
        message = file_name + " " + method_name + " " + error_contant

        log=Log()
        log.error_log(message)
        raise HTTPException(status_code=error.InternalServer.status_code,
                            detail={"type": error.InternalServer.detail,
                                    "msg": error_contant})

    
    db.commit()


"""
ユーザーの編集
"""
def edit_user(db:Session, value:users_schema.UpdateUserInfo):

    search_info = users_schema.SearchUserSearch()
    search_info.user_id = value.user_id
    if value.is_usage == None:
        search_info.is_usage = False

    target_user = get_prefix_user(db=db,value=search_info)

    if target_user == None:

        file_name = "file: " +  __file__
        method_name = "method: " + sys._getframe().f_code.co_name
        error_contant = error_message.not_exist + " User"
        message = file_name + " " + method_name + " " + error_contant

        log=Log()
        log.error_log(message)
        raise HTTPException(status_code=error.DataNotFound.status_code,
                            detail={"type": error.DataNotFound.detail,
                                    "msg": error_contant})

    if value.user_name:
        search_info = users_schema.SearchUserSearch()
        search_info.user_name = value.user_name
        exist_same_name = get_prefix_user(db=db,value=search_info)
    
    if exist_same_name:
        file_name = "file: " +  __file__
        method_name = "method: " + sys._getframe().f_code.co_name
        error_contant = error_message.already_existed + " User"
        message = file_name + " " + method_name + " " + error_contant

        log=Log()
        log.error_log(message)
        raise HTTPException(status_code=error.Conflict.status_code,
                            detail={"type": error.Conflict.detail,
                                    "msg": error_contant})
    try:
        if value.user_name:
            target_user.name = value.user_name

        if value.password:
            target_user.password = value.password

        if value.is_usage:
            if target_user.is_usage == flag_value.is_usage:
                target_user.is_usage = flag_value.not_usage

            elif target_user.is_usage == flag_value.not_usage:
                target_user.is_usage = flag_value.is_usage

        db.flush()

    except:
        file_name = "file: " +  __file__
        method_name = "method: " + sys._getframe().f_code.co_name
        error_contant = error_message.update_error + " User"
        message = file_name + " " + method_name + " " + error_contant

        log=Log()
        log.error_log(message)
        raise HTTPException(status_code=error.InternalServer.status_code,
                            detail={"type": error.InternalServer.detail,
                                    "msg": error_contant})

    
    db.commit()