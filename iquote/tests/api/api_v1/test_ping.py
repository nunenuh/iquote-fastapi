# project/tests/test_ping.py

# from app import main
from fastapi.testclient import TestClient


def test_ping(client: TestClient):
    # Given
    # test_app

    # When
    response = client.get("api/v1/ping")

    # Then
    assert response.status_code == 200
    assert response.json() == {"environment": "dev", "ping": "pong!", "testing": True}
