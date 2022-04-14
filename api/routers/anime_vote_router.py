from typing import List
from typing import Optional

from fastapi import APIRouter
from fastapi import Body
from fastapi import Depends
from fastapi import status
from fastapi.security import OAuth2PasswordBearer
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from database_setting import get_db
from schemas import anime_vote_schema
from database import anime_vote_db


router = APIRouter()
tag_name = ['vote']
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/animevote", tags=tag_name, response_model=List[anime_vote_schema.AnimeVoteBase], status_code=status.HTTP_200_OK)
def list_vote(db: Session = Depends(get_db),):
    data = anime_vote_db.get_vote_all(db)
    data_to_json = jsonable_encoder(data)
    return JSONResponse(content={'status_code': 200, 'data': data_to_json})

@router.get("/animevote/ranking", tags=tag_name, response_model=List[anime_vote_schema.AnimeVoteRank])
def get_specific_votes(db: Session = Depends(get_db),
                       limit : Optional[int] = None,
                       skip : Optional[int] = None,
                       filter:Optional[str] = None
                       ):
    """
    limit  : 件数の指定\n
    skip   : スキップ件数\n
    filter : 特定のID指定
    """

    if(filter is not None):
        split_filter = filter.split(',')
        filter_tO_int = [int(s) for s in split_filter]
    else:
        filter_tO_int = []

    data = anime_vote_db.get_ranking(db,limit,skip,filter_tO_int)
    data_to_json = jsonable_encoder(data)
    return JSONResponse(content={'status_code': 200, 'data':data_to_json})



@router.post("/animevote/vote", tags=tag_name, response_model=anime_vote_schema.AnimeVoteBase)
def create_vote(vote: anime_vote_schema.CreateVote,db: Session = Depends(get_db)):

    data = anime_vote_db.create_vote(db=db,vote=vote)
    data_to_json = jsonable_encoder(data)
    return JSONResponse(content={'status_code': 200, 'data':data_to_json})