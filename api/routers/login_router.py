from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database_setting import get_db
from models import user_model
from schemas import login_schema
from cruds import login_crud

router = APIRouter()

@router.post("/token", response_model=login_schema.Token)
def login(form: OAuth2PasswordRequestForm = Depends(),db:Session = Depends(get_db)):
    """トークン発行"""
    user = login_crud.authenticate(form.username, form.password,db)
    return login_crud.create_tokens(user.user_id,db)

@router.get("/refresh_token/", response_model=login_schema.Token)
def refresh_token(current_user: user_model.User = Depends(login_crud.get_current_user_with_refresh_token)):
    """リフレッシュトークンでトークンを再取得"""
    return login_crud.create_tokens(current_user.id)

@router.get("/users/me/", response_model= login_schema.User)
def read_users_me(current_user: user_model.User = Depends(login_crud.get_current_user),):
    """ログイン中のユーザーを取得"""
    return current_user


"""
scope とは？
⇒権限の値 

"""