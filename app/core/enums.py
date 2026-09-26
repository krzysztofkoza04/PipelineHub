from enum import Enum


class SourceType(str, Enum):
    CSV = "csv"
    JSON = "json"
    API = "api"
    POSTGRESQL = "postgresql"


class PipelineStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    ARCHIVED = "archived"