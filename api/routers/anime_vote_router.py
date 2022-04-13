from typing import List
from typing import Optional
from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from database_setting import get_db
from schemas import anime_vote_schema
from database import anime_vote_db


router = APIRouter()
tag_name = ['vote']
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



@router.get("/animevote", tags=tag_name, response_model=List[anime_vote_schema.AnimeVoteBase])
def list_vote(db: Session = Depends(get_db)):
    return anime_vote_db.get_vote_all(db)

@router.get("/animevote/ranking", tags=tag_name, response_model=List[anime_vote_schema.AnimeVoteRank])
def get_specific_votes(db: Session = Depends(get_db),
                       limit : Optional[int] = None,
                       skip : Optional[int] = None,
                       filter:Optional[str] = None
                       ):
    if (limit is not None and skip is not None and filter is None):
        return anime_vote_db.get_vote_limit_skip_ranking(db,limit,skip)
    elif(filter is not None):
        filterSplit = filter.split(',')
        filterListToInt = [int(s) for s in filterSplit]
        return anime_vote_db.get_vote_limit_skip_filterlist_ranking(db,limit,skip,filterListToInt)
    else:
        print(9)
        return []


@router.post("/animevote/vote", tags=tag_name, response_model=anime_vote_schema.AnimeVoteBase)
def create_vote(vote: anime_vote_schema.CreateVote,db: Session = Depends(get_db)):
    return anime_vote_db.create_vote(db=db,vote=vote)
