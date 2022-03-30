import datetime
import ipaddress
from typing import Optional
from pydantic import BaseModel
from pydantic import Field

class AnimeVoteBase(BaseModel):
    anime_id: Optional[int] = Field(None,example=1)

    #これがないとSQLAlchemy 実行でerror500になる
    class Config:
        orm_mode = True
    
class AnimeVoteRank(AnimeVoteBase):
    rank: Optional[int]= Field(None, example=1)
    vote_count: Optional[int] = Field(None, example=1)
    class Config:
        orm_mode = True

class CreateVote(AnimeVoteBase):
    user_id  : Optional[str] = Field(None,example="1111")
    ipaddress: Optional[str] = Field(None,example="192.168.0.0")
    # create_at: datetime.datetime = Field(None, example=datetime.datetime.now())
    # update_at: datetime.datetime = Field(None, example=datetime.datetime.now())
    class Config:
        orm_mode = True
# class AnimeVoteCreate(AnimeVoteBase):
#     create_at: Optional[int]= Field(None, example=1)
#     update_at: Optional[int] = Field(None, example=1)
#     class Config:
#         orm_mode = True