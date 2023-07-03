# project/tests/test_ping.py

from app import main


def test_health_full(test_app):
    # Given
    # test_app

    # When
    response = test_app.get("api/v1/health")
    response_json = response.json()

    # Then
    assert response.status_code == 200
    assert response_json['status'] == "Healthy"

def test_health_live(test_app):
    # Given
    # test_app

    # When
    response = test_app.get("api/v1/health/live")
    
    # Then
    assert response.status_code == 200
    assert response.json() == {"status":"OK"}


def test_health_ready(test_app):
    # Given
    # test_app

    # When
    response = test_app.get("api/v1/health/ready")

    # Then
    assert response.status_code == 200
    assert response.json() == {"status":"OK"}
    
def test_health_started(test_app):
    # Given
    # test_app

    # When
    response = test_app.get("api/v1/health/started")

    # Then
    assert response.status_code == 200
    assert response.json() == {"status":"OK"}