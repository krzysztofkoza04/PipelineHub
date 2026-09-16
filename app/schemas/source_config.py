from typing import Any, Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    HttpUrl,
    ValidationError,
)

from app.core.enums import SourceType


class CSVSourceConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    path: str = Field(min_length=1)
    delimiter: str = Field(
        default=",",
        min_length=1,
        max_length=1,
    )
    encoding: str = "utf-8"


class JSONSourceConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    path: str = Field(min_length=1)
    encoding: str = "utf-8"


class APISourceConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    url: HttpUrl
    method: Literal["GET", "POST"] = "GET"


class PostgreSQLSourceConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    host: str = Field(min_length=1)
    port: int = Field(
        default=5432,
        ge=1,
        le=65535,
    )
    database: str = Field(min_length=1)
    username: str = Field(min_length=1)


def validate_source_config(
    source_type: SourceType,
    config: dict[str, Any],
) -> dict[str, Any]:

    try:
        if source_type == SourceType.CSV:
            validated = CSVSourceConfig.model_validate(config)

        elif source_type == SourceType.JSON:
            validated = JSONSourceConfig.model_validate(config)

        elif source_type == SourceType.API:
            validated = APISourceConfig.model_validate(config)

        elif source_type == SourceType.POSTGRESQL:
            validated = PostgreSQLSourceConfig.model_validate(config)

        else:
            raise ValueError("Unsupported source type")

    except ValidationError as exc:
        raise ValueError(str(exc)) from exc

    return validated.model_dump(mode="json")