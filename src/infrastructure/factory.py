from typing import cast

from httpx import AsyncClient


def create_http_client(
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
