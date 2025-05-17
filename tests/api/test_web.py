import pytest
from fastapi.testclient import TestClient


@pytest.mark.parametrize(
    "endpoint", [("/"), ("healthz"), ("readyz"), ("livez"), ("startupz")]
)
@pytest.mark.anyio
def test_basic_endpoint(
    fake_chat_client: TestClient,
    endpoint: str,
) -> None:
    response = fake_chat_client.get(endpoint)
    assert response.status_code == 200
    assert response.json() == {"status": "OK"}
