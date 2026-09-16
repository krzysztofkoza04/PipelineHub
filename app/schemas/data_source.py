from datetime import datetime
from typing import Any
from pydantic import BaseModel, ConfigDict, Field

from app.core.enums import SourceType


class DataSourceCreate(BaseModel):
    name: str = Field(min_length=3, max_length=200)
    source_type: SourceType
    config: dict[str,Any] = Field(default_factory = dict)


class DataSourceUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=3,
        max_length=200,
    )
    source_type: SourceType | None = None
    config : dict[str,Any] | None = None


class DataSourceRead(BaseModel):
    id: int
    project_id: int
    name: str
    source_type: SourceType
    config : dict[str, Any]
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )