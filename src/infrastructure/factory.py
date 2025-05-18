from typing import cast

from httpx import AsyncClient
from loguru import logger


def create_http_client(
    api_key: str | None,
    base_url: str | None,
) -> AsyncClient | None:
    logger.debug(api_key)
    if api_key is None:
        return None

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    return AsyncClient(
        headers=headers,
        base_url=cast(str, base_url),
    )
