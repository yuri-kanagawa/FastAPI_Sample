from fastapi import FastAPI
from routers import anime_vote_router
import graphene_sqlalchemy
# from routers import bbs_list
from routers import login_router


app = FastAPI()

app.include_router(anime_vote_router.router)
app.include_router(login_router.router)