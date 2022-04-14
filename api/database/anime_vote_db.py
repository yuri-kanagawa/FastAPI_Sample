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
    parametr : 無
    全投票結果取得
    """
    #SQLAlcgemy 記述
    return db.query(anime_vote_model.AnimeVote.anime_id).all()


def get_ranking(db:Session, limit: int, skip:int, filter:List[int]):
    """"
    limit  : 件数の指定
    skip   : スキップ件数
    filter : 特定のID指定
    """

    query = db.query(
        func.row_number().
            over(
                order_by=desc(func.count(anime_vote_model.AnimeVote.anime_id))
            ).label('rank'),
            anime_vote_model.AnimeVote.anime_id,
            func.count(anime_vote_model.AnimeVote.anime_id).label('vote_count')
        ).\
        group_by(anime_vote_model.AnimeVote.anime_id)

    #パラメータ1つ
    if(limit is not None and skip is None and filter == []):
        return query.limit(limit).all()
    
    if(limit is None and skip is not None and filter == []):
        return query.offset(skip).all()

    if(limit is None and  skip is None and filter != []):
        return query.filter(anime_vote_model.AnimeVote.anime_id.in_(filter)).all()


    #パラメータ2つ
    #パラメータ2つはこのパターン以外使わなさそう
    if(limit is not None and skip is not None and filter == []):
        return query.\
                limit(limit).\
                offset(skip).\
                all()

    if(limit is not None and skip is None and filter != []):
        return query.filter(anime_vote_model.AnimeVote.anime_id.in_(filter)).\
                limit(limit).\
                all()

    if(limit is None and skip is not None and filter != []):
        return query.filter(anime_vote_model.AnimeVote.anime_id.in_(filter)).\
                offset(skip).\
                all()

    #パラメータ3つ
    if(limit is not  None and  skip is not None and filter != []):
        return query.filter(anime_vote_model.AnimeVote.anime_id.in_(filter)).\
                limit(limit).\
                offset(skip).\
                all()


def create_vote(db:Session,vote:anime_vote_schema.CreateVote) -> anime_vote_model.AnimeVote:
    vote_time = datetime.datetime.now()
    db_vote =  anime_vote_model.AnimeVote(anime_id=vote.anime_id,user_id=vote.user_id,ipaddress=vote.ipaddress,create_at=vote_time,update_at=vote_time)
    db.add(db_vote)
    db.commit()
    db.refresh(db_vote)
    return vote.anime_id