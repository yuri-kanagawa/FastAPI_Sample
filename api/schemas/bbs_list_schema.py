from ctypes.wintypes import tagMSG
import datetime
from doctest import Example
from ipaddress import ip_address
from typing import Optional
from pydantic import BaseModel
from pydantic import Field

class BbsListBase(BaseModel):
    bbs_list_id: Optional[int] = Field(None,example=1)
    bbs_title  : Optional[str] = Field(None,example="タイトル")
    anime_id   : Optional[int] = Field(None,example="")
    tag        : Optional[str] = Field(None,example="")
    user_id    : Optional[str] = Field(None,example="")
    ipaddress  : Optional[str] = Field(None,example="192.168.0.0")
    class Config:
        orm_mode = True
    
