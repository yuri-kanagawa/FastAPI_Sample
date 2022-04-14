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