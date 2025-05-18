from enum import StrEnum, auto
from pathlib import Path

from openai import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class ServiceName(StrEnum):
    SIMPLE_CHAT = auto()  # simple graph application for test


class OpenaiSettings(BaseModel):
    api_key: str | None = None
    base_url: str | None = None


class InfrastructureSetttings(BaseModel):
    openai: OpenaiSettings


class Settings(BaseSettings):
    service_name: ServiceName
    graph_spec_path: Path
    infrastructure: InfrastructureSetttings

    model_config = SettingsConfigDict(
        env_file=Path(".env"),
        env_prefix="SJYB_AGENT_",
        env_nested_delimiter="__",
        extra="ignore",
    )
