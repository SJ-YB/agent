from fastapi.testclient import TestClient
import pytest

from src.api.web.app import create_web_app


@pytest.fixture(scope="session")
def client() -> TestClient:
    app = create_web_app()
    return TestClient(app)
