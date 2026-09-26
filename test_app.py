import pytest
from app import app, parked_vehicles


@pytest.fixture
def client():
    """Sets up an isolated test client and clears data before each test."""
    app.config["TESTING"] = True
    parked_vehicles.clear()
    with app.test_client() as client:
        yield client


def test_health_check(client):
    """1. Test that /health returns status 200 and 'ok'."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "ok"


def test_park_vehicle_updates_slots(client):
    """2. Test dynamic feature: parking a vehicle decreases available slots."""
    # Park a car
    res = client.post(
        "/park",
        data={"vehicle_no": "MH12AB1234", "vehicle_type": "Car"}
    )
    # Redirects to home page (HTTP 302) upon success
    assert res.status_code == 302

    # Check the API returns updated dynamic state
    api_res = client.get("/api/slots")
    assert api_res.status_code == 200
    data = api_res.get_json()
    assert data["occupied_slots"] == 1
    assert data["available_slots"] == 14
    assert len(data["vehicles"]) == 1
    assert data["vehicles"][0]["vehicle_no"] == "MH12AB1234"


def test_invalid_input_rejected(client):
    """3. Test quality gate: empty vehicle number or invalid type returns 400."""
    # Empty vehicle number
    res1 = client.post(
        "/park",
        data={"vehicle_no": "", "vehicle_type": "Car"}
    )
    assert res1.status_code == 400

    # Invalid vehicle type
    res2 = client.post(
        "/park",
        data={"vehicle_no": "MH12XY9999", "vehicle_type": "Truck"}
    )
    assert res2.status_code == 400