from typing import Optional
from pydantic import BaseModel

# class Token(BaseModel):
#     access_token: str
#     token_type: str
#     class Config:
#         orm_mode = True

# class TokenData(BaseModel):
#     username: Optional[str] = None
#     class Config:
#         orm_mode = True


# class User(BaseModel):
#     user_id:Optional[int]
#     username: Optional[str]
#     email: Optional[str] = None
#     full_name: Optional[str] = None
#     disabled: Optional[str] = None
#     class Config:
#         orm_mode = True


# class UserInDB(User):
#     hashed_password: str
#     class Config:
#         orm_mode = True
class Token(BaseModel):
    access_token: Optional[str]
    refresh_token: Optional[str]
    token_type: Optional[str]

    class Config:
        orm_mode = True

class User(BaseModel):
    name: Optional[str]

    class Config:
        orm_mode = True