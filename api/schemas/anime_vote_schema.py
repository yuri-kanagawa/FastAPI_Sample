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

class CreateVote(AnimeVoteBase):
    user_id  : Optional[str] = Field(None,example="1111")
    ipaddress: Optional[str] = Field(None,example="192.168.0.0")

