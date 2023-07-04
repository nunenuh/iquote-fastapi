# project/tests/test_ping.py

from fastapi.testclient import TestClient

def test_health_full(client: TestClient):
    # Given
    # test_app

    # When
    response = client.get("api/v1/health")
    response_json = response.json()

    # Then
    assert response.status_code == 200
    assert response_json['status'] == "Healthy"

def test_health_live(client: TestClient):
    # Given
    # test_app

    # When
    response = client.get("api/v1/health/live")
    
    # Then
    assert response.status_code == 200
    assert response.json() == {"status":"OK"}


def test_health_ready(client: TestClient):
    # Given
    # test_app

    # When
    response = client.get("api/v1/health/ready")

    # Then
    assert response.status_code == 200
    assert response.json() == {"status":"OK"}
    
def test_health_started(client: TestClient):
    # Given
    # test_app

    # When
    response = client.get("api/v1/health/started")

    # Then
    assert response.status_code == 200
    assert response.json() == {"status":"OK"}