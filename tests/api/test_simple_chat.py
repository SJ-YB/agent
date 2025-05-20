from fastapi.testclient import TestClient


def test_chat_endpoint_response(
    fake_chat_client: TestClient,
) -> None:
    response = fake_chat_client.post(
        url="/api/v1/chat",
        json={
            "id": "test_id",
            "thread_id": "test_thread",
            "message": "test message",
        },
    )
    assert response.status_code == 200
    assert response.json() == {"id": "test_id", "message": "fake response"}
