from typing import cast

from httpx import AsyncClient, Client
from langchain_openai import OpenAI
from openai import AsyncOpenAI


def create_async_openai_client(
    enabled: bool,
    api_key: str | None,
    base_url: str | None,
) -> AsyncOpenAI | None:
    if not enabled:
        return None

    return AsyncOpenAI(
        api_key=api_key,
        base_url=base_url,
    )


def create_sync_openai_client(
    enabled: bool,
    api_key: str | None,
    base_url: str | None,
) -> OpenAI | None:
    if not enabled:
        return None

    return OpenAI(
        api_key=api_key,
        base_url=base_url,
    )


def create_async_http_client(
    enabled: bool,
    api_key: str | None,
    base_url: str | None,
) -> AsyncClient | None:
    if not enabled:
        return None

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    return AsyncClient(
        headers=headers,
        base_url=cast(str, base_url),
    )


def create_sync_http_client(
    enabled: bool,
    api_key: str | None,
    base_url: str | None,
) -> Client | None:
    if not enabled:
        return None

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    return Client(
        headers=headers,
        base_url=cast(str, base_url),
    )
