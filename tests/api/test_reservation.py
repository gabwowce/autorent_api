"""
app/tests/test_reservation.py

Automated tests for Reservation API endpoints.

Author: Vytautas Petronis <vytautas.petronis@stud.viko.lt>

Description:
    This test module contains integration tests for the /reservations endpoints
    of the Car Rental RESTful API. The tests cover reservation creation,
    retrieval, listing, and deletion operations using FastAPI TestClient.

Usage:
    Run these tests with pytest:
        pytest tests/test_reservation.py
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.fixture
def example_reservation_data():

    """
    Example reservation data fixture for reservation tests.

    Returns:
        dict: Dictionary with sample reservation data.

    Author: Vytautas Petronis <vytautas.petronis@stud.viko.lt>
    """

    return {
        "kliento_id": 1,
        "automobilio_id": 1,
        "rezervacijos_pradzia": "2024-06-01",
        "rezervacijos_pabaiga": "2024-06-03",
        "busena": "aktyvi"
    }

def test_create_reservation(example_reservation_data):

    """
    Test creation of a new reservation.

    Args:
        example_reservation_data (dict): Fixture with reservation data.

    Author: Vytautas Petronis <vytautas.petronis@stud.viko.lt>
    """

    response = client.post("/api/v1/reservations/", json=example_reservation_data)
    assert response.status_code == 200 or response.status_code == 201
    data = response.json()
    assert "rezervacijos_id" in data
    assert data["kliento_id"] == example_reservation_data["kliento_id"]
    assert data["automobilio_id"] == example_reservation_data["automobilio_id"]

def test_get_all_reservations():

    """
    Test retrieval of all reservations.

    Author: Vytautas Petronis <vytautas.petronis@stud.viko.lt>
    """    

    response = client.get("/api/v1/reservations/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_reservation_by_id():

    """
    Test retrieving a reservation by its ID.

    Author: Vytautas Petronis <vytautas.petronis@stud.viko.lt>
    """

    res_resp = client.post("/api/v1/reservations/", json={
        "kliento_id": 1,
        "automobilio_id": 1,
        "rezervacijos_pradzia": "2024-06-01",
        "rezervacijos_pabaiga": "2024-06-03",
        "busena": "aktyvi"
    })
    res_id = res_resp.json()["rezervacijos_id"]
    # Gaunam pagal ID
    get_resp = client.get(f"/api/v1/reservations/{res_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["rezervacijos_id"] == res_id

def test_delete_reservation():

    """
    Test deleting a reservation and verifying its removal.

    Author: Vytautas Petronis <vytautas.petronis@stud.viko.lt>
    """

    res_resp = client.post("/api/v1/reservations/", json={
        "kliento_id": 1,
        "automobilio_id": 1,
        "rezervacijos_pradzia": "2024-06-01",
        "rezervacijos_pabaiga": "2024-06-03",
        "busena": "aktyvi"
    })
    res_id = res_resp.json()["rezervacijos_id"]
    # Trinam
    del_resp = client.delete(f"/api/v1/reservations/{res_id}")
    assert del_resp.status_code == 200 or del_resp.status_code == 204
    # Patikrinam, ar ištrinta
    get_all = client.get("/api/v1/reservations/").json()
    ids = [r["rezervacijos_id"] for r in get_all]
    assert res_id not in ids
