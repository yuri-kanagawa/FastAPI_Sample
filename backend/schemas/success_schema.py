from pydantic import BaseModel
from pydantic import Field

class ReponseSuccess(BaseModel):
    status_code:int = Field(example=200)
