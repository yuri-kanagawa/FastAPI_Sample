from typing import Optional


from pydantic import BaseModel
from pydantic import Field

class ThreadBase(BaseModel):
    thread_id: Optional[int] = Field(None, example=1)
    response_id: Optional[int] = Field(None, example=1)
    name: Optional[str] = Field(None, example='name')
    content: Optional[str] = Field(None, example='contant')
    image: Optional[str] = Field(None, example='imageDirectory')
    user_id: Optional[str] = Field(None, example='user_id')
    ipaddress: Optional[str] = Field(None, example='192.168.40.128')
    

    class Config:
        orm_mode = True        