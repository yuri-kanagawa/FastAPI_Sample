from fastapi import FastAPI
from fastapi import APIRouter

from routers import anime_vote_router
from routers import login_router
from routers import image_router


app = FastAPI()

# @app.get("/")
# async def read_main():
#     return {"msg": "Hello World"}

app.include_router(anime_vote_router.router)
app.include_router(login_router.router)
app.include_router(image_router.router)