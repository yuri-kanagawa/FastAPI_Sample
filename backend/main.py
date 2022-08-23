from fastapi import FastAPI
# from fastapi.staticfiles import StaticFiles

from routers import bbs_threads_router
from routers import users_router


description="""
SampleAPI Description
"""

app = FastAPI(
    title="SampleFastAPI",
    description=description,
    version="0.0.1",
    contact={
        "name": "Yuri Kanagwa",
        "url": "https://yurikanagawa.com/",
    },
)

app.include_router(users_router.router)
app.include_router(bbs_threads_router.router)

# app.mount('/files', StaticFiles(directory="files"), name='files')