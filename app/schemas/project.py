from datetime import datetime

from pydantic import BaseModel,  ConfigDict,  Field

class ProjectCreate(BaseModel):
    name: str = Field(
        min_length=3,
        max_length=200,
    )
    description : str | None= Field(
        default=None,
        max_length=1000,
    )


class ProjectRead(BaseModel):
    id:int
    name:str
    description:str|None
    created_at : datetime

    model_config=ConfigDict(form_attributes=True)



class ProjectUpdate(BaseModel):
    name : str | None = Field(
        default=None,
        min_length=3,
        max_length=200,
    )
    description: str | None  = Field(
        default=None,
        max_length=1800,
    )

    