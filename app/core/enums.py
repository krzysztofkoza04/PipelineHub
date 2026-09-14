from enum import Enum


class SourceType(str, Enum):
    CSV = "csv"
    JSON = "json"
    API = "api"
    POSTGRESQL = "postgresql"