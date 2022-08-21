import json
from typing import Union
from typing import List

from fastapi import UploadFile
from fastapi import Query
from pydantic import BaseModel
from pydantic import Field


class RequestBodyCreateBbs(BaseModel):
    bbs_thread_title:str = Field(default=..., max_length=20)
    post_user_name: str = Field(default=..., max_length=10)

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


class CreateBbsThread():
    thread_title:str
    post_user_name:str
    image_file: Union[UploadFile,None] = None
    user_id:int


class RequestQueryReadBbsThreadBase(BaseModel):
    thread_id: Union[int, None] = Query(default=None)
    thread_title: Union[str, None] = Query(default=None, max_length=20)
    post_user_name: Union[str, None] = Query(default=None)
    is_usage: Union[bool, None] = Query(default=None)

class SearchGetBbsThread():
    thread_id:Union[int,None] = None
    strict_thread_title: Union[str, None] = None
    like_thread_title: Union[str, None] = None
    post_user_name: Union[str, None] = None
    is_usage: Union[bool, None] = None

class ResponseReadBbsThreadBase(BaseModel):
    status_code:int = Field(example=200)
    data:List[dict] = Field(example=[{"thread_id":1,
                                        "thread_title": "bbs_thread_title",
                                        "post_user_name": "post_user_name",
                                        "account_user_name": "user_name",
                                        "file_path": "file_path",
                                        "is_usage": True}])