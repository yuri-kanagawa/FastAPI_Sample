
from typing import List
from typing import Union

from fastapi import Query
from pydantic import BaseModel
from pydantic import Field

class RequestBodyCreateUserBase(BaseModel):
    user_name:str = Field(default=..., example="UserName", max_length=20)
    password:str = Field(default=..., example="password")

class RequestBodyLoginUserBase(BaseModel):
    user_name:str = Field(default=..., example="UserName", max_length=20)
    password:str = Field(default=..., example="password")

class ResponseBodyLoginBase(BaseModel):
    status_code:int = Field(example=200)
    data:dict = Field(example={"user_id":1,
                                "user_name": "UserName",
                                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                                "refresh_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."})

class SearchUserSearch():
    user_id: Union[int, None] = None
    user_name: Union[str, None] = None
    password: Union[str, None] = None
    is_usage: Union[str, None] = None
    refresh_token: Union[str, None] = None

class RequestQueryReadUserBase(BaseModel):
    user_id: Union[int, None] = Query(default=None)
    user_name: Union[str, None] = Query(default=None)
    is_usage: Union[bool, None] = Query(default=None)


class ReponseReadUserBase(BaseModel):
    status_code:int = Field(example=200)
    data:List[dict] = Field(example=[{"user_id":1,"user_name":"ユーザー名"}])

class RequestBodyUpdateUserInfo(BaseModel):
    user_name: Union[str, None] = Field(default=None, example="UserName", max_length=20)
    password: Union[str,None] = Field(default=None, example="Password")

class UpdateUserInfo():
    user_id:int
    user_name: Union[str, None] = None
    password: Union[str,None] = None
    is_usage: Union[bool, None] = None

class ResponseTokenBase(BaseModel):
    status_code:int = Field(example=200)
    data:dict = Field(example={"access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6Ik",
                                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6Ik"})