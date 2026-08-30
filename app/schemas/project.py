from datetime import datetime

from pydantic import BaseModel,  ConfigDict

class ProjectCreate(BaseModel):
    name: str
    description : str | None=None


class ProjectRead(BaseModel):
    id:int
    name:str
    description:str|None
    created_at : datetime

    model_config=ConfigDict(form_attributes=True)

    