from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.core.enums import PipelineStatus


class PipelineCreate(BaseModel):
    name: str = Field(
        min_length=3,
        max_length=200,
    )

    description: str | None = Field(
        default=None,
        max_length=1000,
    )


class PipelineUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=3,
        max_length=200,
    )

    description: str | None = Field(
        default=None,
        max_length=1000,
    )

    status: PipelineStatus | None = None


class PipelineRead(BaseModel):
    id: int
    project_id: int
    name: str
    description: str | None
    status: PipelineStatus
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )