from enum import StrEnum, auto
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class ServiceName(StrEnum):
    SIMPLE_CHAT = auto()  # simple graph application for test


class Settings(BaseSettings):
    service_name: ServiceName
    graph_spec_path: Path

    model_config = SettingsConfigDict(
        env_file=Path(".env"),
        env_prefix="RNC_AGENT_",
        env_nested_delimiter="__",
        extra="ignore",
    )
