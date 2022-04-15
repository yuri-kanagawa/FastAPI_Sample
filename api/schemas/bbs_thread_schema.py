import inspect
from typing import Optional
from typing import Type

from fastapi import File
from fastapi import Form
from fastapi import UploadFile
from pydantic import BaseModel
from pydantic import Field

def as_form(cls: Type[BaseModel]):
    """
    Adds an as_form class method to decorated models. The as_form class method
    can be used with FastAPI endpoints
    """
    new_params = [
        inspect.Parameter(
            field.alias,
            inspect.Parameter.POSITIONAL_ONLY,
            default=(Form(field.default) if not field.required else Form(...)),
            annotation=field.outer_type_,
        )
        for field in cls.__fields__.values()
    ]

    async def _as_form(**data):
        return cls(**data)

    sig = inspect.signature(_as_form)
    sig = sig.replace(parameters=new_params)
    _as_form.__signature__ = sig
    setattr(cls, "as_form", _as_form)
    return cls

@as_form
class ThreadBase(BaseModel):
    # thread_id: Optional[int] = Field(None, example=1)
    thread_title: Optional[str] = Field(None, example='title')
    tag: Optional[str] = Field(None, example='tag')
    anime_id: Optional[int] = Field(None, example=1)
    # image: Optional[str] = Field(None, example='image_directory')
    user_id: Optional[str] = Field(None, example='image_directory')
    ipaddress: Optional[str] = Field(None, example='192.168.110')
    # image_file:Optional[UploadFile] = File(None)

    class Config:
        orm_mode = True        
    