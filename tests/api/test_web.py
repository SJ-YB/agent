import pytest
from fastapi.testclient import TestClient


@pytest.mark.parametrize(
    "endpoint", [("/"), ("healthz"), ("readyz"), ("livez"), ("startupz")]
)
@pytest.mark.anyio
def test_default_endpoint(client: TestClient, endpoint: str) -> None:
    response = client.get(endpoint)
    assert response.status_code == 200
    assert response.json() == {"status": "OK"}
