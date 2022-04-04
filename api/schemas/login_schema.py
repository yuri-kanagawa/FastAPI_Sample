from typing import Optional

from pydantic import BaseModel

class Token(BaseModel):
    access_token: Optional[str]
    refresh_token: Optional[str]
    token_type: Optional[str]

    class Config:
        orm_mode = True

class User(BaseModel):
    name: Optional[str]

    class Config:
        orm_mode = True