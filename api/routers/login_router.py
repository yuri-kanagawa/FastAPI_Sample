from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database_setting import get_db
from models import user_model
from schemas import login_schema
from database import login_db

router = APIRouter()

tag_name = ['login/logout']

@router.post("/token", tags = tag_name, response_model=login_schema.Token)
def login(form: OAuth2PasswordRequestForm = Depends(),db:Session = Depends(get_db)):
    """トークン発行"""
    user = login_db.authenticate(form.username, form.password,db)
    return login_db.create_tokens(user.user_id,db)

@router.get("/refresh", tags = tag_name, response_model= login_schema.User)
def read_users_me(current_user: user_model.User = Depends(login_db.get_current_user)):
    """ログイン中のユーザーを取得"""
    return current_user

# @router.post("/logout", tags = tag_name, response_model=login_schema.Token)
# def logout(session: Session = Depends(supertokens_session)):
#     session.revoke_session()
#     return JSONResponse({})