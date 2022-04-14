from typing import Optional

from pydantic import BaseModel
from pydantic import Field

class ThreadBase(BaseModel):
    thread_id: Optional[int] = Field(None, example=1)
    thread_title: Optional[int] = Field(None, example='title')
    tag: Optional[str] = Field(None, example='tag')
    anime_id: Optional[int] = Field(None, example='1')
    image: Optional[str] = Field(None, example='image_directory')
    user_id: Optional[str] = Field(None, example='image_directory')
    ipaddress: Optional[str] = Field(None, example='ipaddress')

    class Config:
        orm_mode = True        
    