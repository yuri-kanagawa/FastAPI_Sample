from typing import Optional
from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, status
from datetime import datetime, timedelta
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from database_setting import get_db
from passlib.context import CryptContext
from schemas import login_schema
from cruds import login_crud
from models import user_model

router = APIRouter()
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# #SECRET_KEY = "b1a48cd25b66509fd608f28af313cdd0ddc3d662b715d20b911a1b85241089a0"
# SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30

# @router.post("/token", response_model=login_schema.Token)
# def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
#     user = authenticate_user(form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.username}, expires_delta=access_token_expires
#     )
#     return {"access_token": access_token, "token_type": "bearer"}


# def authenticate_user(username: str, password: str,db: Session = Depends(get_db)):

#     user = login_crud.get_user(db, username)
#     if not user:
#         return False
#     if not verify_password(password, user.hashed_password):
#         return False
#     return user

# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)

# def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt

@router.post("/token", response_model=login_schema.Token)
def login(form: OAuth2PasswordRequestForm = Depends(),db:Session = Depends(get_db)):
    """トークン発行"""
    user = login_crud.authenticate(form.username, form.password,db)
    return login_crud.create_tokens(user.user_id)

@router.get("/refresh_token/", response_model=login_schema.Token)
def refresh_token(current_user: user_model.User = Depends(login_crud.get_current_user_with_refresh_token)):
    """リフレッシュトークンでトークンを再取得"""
    return login_crud.create_tokens(current_user.id)

@router.get("/users/me/", response_model= login_schema.User)
def read_users_me(current_user: user_model.User = Depends(login_crud.get_current_user)):
    """ログイン中のユーザーを取得"""
    return current_user

"""
scope とは？
⇒権限の値 

"""