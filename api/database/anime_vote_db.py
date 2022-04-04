import datetime
from typing import List, Tuple
from typing import Tuple

from sqlalchemy import func,desc
from sqlalchemy import desc
from sqlalchemy.orm import Session

from models import anime_vote_model
from schemas import anime_vote_schema


def get_vote_all(db: Session) -> List[Tuple[int, int]]:
    """
    SQL 記述
    result: Result = (
        db.execute(
            select(
                anime_vote_model.AnimeVote.vote_id,
                anime_vote_model.AnimeVote.anime_id
            )
        )
    )
    return result.all()
    """
    #SQLAlcgemy 記述
    return db.query(anime_vote_model.AnimeVote).all()

def get_vote_limit_skip_ranking(db:Session,limit: int,skip:int):
    return db.query(
        func.row_number().
            over(
                order_by=desc(func.count(anime_vote_model.AnimeVote.anime_id))
            ).label('rank'),
            anime_vote_model.AnimeVote.anime_id,
            func.count(anime_vote_model.AnimeVote.anime_id).label('vote_count')
        ).\
        group_by(anime_vote_model.AnimeVote.anime_id).\
        limit(limit).\
        offset(skip).\
        all()

def get_vote_limit_skip_filter_ranking(db:Session,filter:int):

    return db.query(
        func.row_number().
            over(
                order_by=desc(func.count(anime_vote_model.AnimeVote.anime_id))
            ).label('rank'),
            anime_vote_model.AnimeVote.anime_id,
            func.count(anime_vote_model.AnimeVote.anime_id).label('vote_count')
        ).\
        filter_by(anime_vote_model.AnimeVote.anime_id.in_(filter)).\
        group_by(anime_vote_model.AnimeVote.anime_id).\
        first()

def get_vote_limit_skip_filterlist_ranking(db:Session,limit: int,skip:int,filterList:List[int]):
        
    return db.query(
        func.row_number().
            over(
                order_by=desc(func.count(anime_vote_model.AnimeVote.anime_id))
            ).label('rank'),
            anime_vote_model.AnimeVote.anime_id,
            func.count(anime_vote_model.AnimeVote.anime_id).label('vote_count')
        ).\
        group_by(anime_vote_model.AnimeVote.anime_id).\
        filter(anime_vote_model.AnimeVote.anime_id.in_(filterList)).\
        limit(limit).\
        offset(skip).\
        all()


def create_vote(db:Session,vote:anime_vote_schema.CreateVote) -> anime_vote_model.AnimeVote:
    vote_time = datetime.datetime.now()
    db_vote =  anime_vote_model.AnimeVote(anime_id=vote.anime_id,user_id=vote.user_id,ipaddress=vote.ipaddress,create_at=vote_time,update_at=vote_time)
    db.add(db_vote)
    db.commit()
    db.refresh(db_vote)
    return db_vote