from fastapi import FastAPI
from fastapi import APIRouter

from routers import anime_vote_router
from routers import bbs_router
from routers import login_router
from routers import image_router


app = FastAPI()

app.include_router(login_router.router)
app.include_router(anime_vote_router.router)
app.include_router(bbs_router.router)
app.include_router(image_router.router)