from typing import List
from typing import Optional
from fastapi import APIRouter
from fastapi import Depends
from schemas import anime_vote_schema
from sqlalchemy.orm import Session
from cruds import anime_vote_crud
from database_setting import get_db

from fastapi.security import OAuth2PasswordBearer

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.get("/animevote", response_model=List[anime_vote_schema.AnimeVoteBase])
def list_vote(db: Session = Depends(get_db)):
    return anime_vote_crud.get_vote_all(db)


@router.get("/animevote/ranking/{limit}{skip}", response_model=List[anime_vote_schema.AnimeVoteRank])
def get_specific_votes(db: Session = Depends(get_db),
                        limit : int = None,
                        skip:int = 0,
                        filter:Optional[str] = None
                        ):

    if (filter is None):
        return anime_vote_crud.get_vote_limit_skip_ranking(db,limit,skip)
    else:
        #まだバグっているよ～
        if filter in ',':
            filterSplit = filter.split(',')
            filterMap = map(int, filterSplit)
            filterList = list(filterMap)
            return anime_vote_crud.get_vote_limit_skip_filterlist_ranking(db,limit,skip,filterList)
        else:
            filterInt = int(filter)
            print(filter)
            return anime_vote_crud.get_vote_limit_skip_filter_ranking(db,limit,skip,filterInt)


# @router.post("/animevote/vote", response_model=anime_vote_schema.AnimeVoteBase)
# def create_vote(vote: anime_vote_schema.CreateVote,db: Session = Depends(get_db)):
#     return anime_vote_crud.create_vote(db=db,vote=vote)

@router.post("/animevote/vote", response_model=anime_vote_schema.AnimeVoteBase)
def create_vote(vote: anime_vote_schema.CreateVote,db: Session = Depends(get_db)):
    return anime_vote_crud.create_vote(db=db,vote=vote)

# @router.get("/test", response_model=List[anime_vote_schema.AnimeVoteBase])
# def test(db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
#     return anime_vote_crud.get_vote_all(db)
