"""
API endpoint tests for Car management (Automobiliai)

Author: Vytautas Petronis <vytautas.petronis@stud.viko.lt>

Description:
    - Integration tests for all /api/v1/cars endpoints.
    - Covers create, read, update, delete, status update, search.
    - Tests happy path, validation, error scenarios, HATEOAS links.

Usage:
    pytest tests/api/test_car.py
"""

import pytest
import uuid

@pytest.fixture(scope="module")
def ensure_place_exists(db_session):
    """
    Ensures that a Location with vietos_id=1 exists in the test database.
    If it does not exist, it creates one. Returns the Location instance.
    """
    from app.models import Location
    vieta = db_session.query(Location).filter_by(vietos_id=1).first()
    if not vieta:
        vieta = Location(vietos_id=1, pavadinimas="Testo vieta", adresas="Test gatvė 1, Miestas", miestas="Vilnius")
        db_session.add(vieta)
        db_session.commit()
    return vieta

CAR_SAMPLE = {
    "marke": "Toyota",
    "modelis": "Corolla",
    "metai": 2022,
    "numeris": "TEST123",
    "vin_kodas": "JH4TB2H26CC000000",
    "spalva": "Mėlyna",
    "kebulo_tipas": "Sedanas",
    "pavarų_deze": "automatinė",
    "variklio_turis": 1.8,
    "galia_kw": 103,
    "kuro_tipas": "benzinas",
    "rida": 10000,
    "sedimos_vietos": 5,
    "klimato_kontrole": True,
    "navigacija": False,
    "kaina_parai": 50.0,
    "automobilio_statusas": "laisvas",
    "technikines_galiojimas": "2025-12-31",
    "dabartine_vieta_id": 1,
    "pastabos": "Test car"
}

@pytest.fixture(scope="module")
def created_car_id(client, ensure_place_exists):
    """
    Creates a new car for use in tests and yields its ID.
    After all tests in the module finish, deletes the created car from the database.
    """
    car_data = CAR_SAMPLE.copy()
    car_data["numeris"] = f"TEST{uuid.uuid4().hex[:6].upper()}"
    car_data["vin_kodas"] = (f"JH4TB2H26{uuid.uuid4().hex[:8].upper()}")[:17]
    resp = client.post("/api/v1/cars/", json=car_data)
    if resp.status_code != 200:
        print(resp.json())
    assert resp.status_code == 200
    car = resp.json()
    yield car["automobilio_id"]
    client.delete(f"/api/v1/cars/{car['automobilio_id']}")

def test_create_car(client, ensure_place_exists):
    """
    Test creating a new car (happy path).
    Verifies the car is created and then deletes it for cleanup.
    """
    car_data = CAR_SAMPLE.copy()
    car_data["numeris"] = f"TEST{uuid.uuid4().hex[:6].upper()}"
    car_data["vin_kodas"] = (f"JH4TB2H26C{uuid.uuid4().hex[:7].upper()}")[:17]
    resp = client.post("/api/v1/cars/", json=car_data)
    if resp.status_code != 200:
        print(resp.json())
    assert resp.status_code == 200
    client.delete(f"/api/v1/cars/{resp.json()['automobilio_id']}")

def test_get_all_cars(client, created_car_id):
    """
    Test retrieving all cars from the API.
    Ensures that the response contains at least one car, including the test car.
    Also checks that every returned car contains HATEOAS links.
    """
    resp = client.get("/api/v1/cars/")
    assert resp.status_code == 200
    cars = resp.json()
    assert isinstance(cars, list)
    assert any(c["automobilio_id"] == created_car_id for c in cars)
    # HATEOAS link check
    assert all("links" in c for c in cars)

def test_get_car_by_id(client, created_car_id):
    """
    Test retrieving a specific car by its ID.
    Verifies that the response contains the correct car and HATEOAS links.
    """
    resp = client.get(f"/api/v1/cars/{created_car_id}")
    assert resp.status_code == 200
    car = resp.json()
    assert car["automobilio_id"] == created_car_id
    assert "links" in car
    # Check some fields
    assert car["marke"] == CAR_SAMPLE["marke"]

def test_get_car_not_found(client):
    """
    Test retrieving a car by a non-existent ID.
    Verifies that the API responds with 404 and an appropriate error message.
    """
    resp = client.get("/api/v1/cars/999999")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Car not found"

def test_update_car(client, created_car_id):
    """
    Test updating a car using PUT.
    Verifies that the car's fields are updated and that HATEOAS links are present in the response.
    """
    update_data = {"marke": "Honda", "modelis": "Civic"}
    resp = client.put(f"/api/v1/cars/{created_car_id}", json=update_data)
    assert resp.status_code == 200
    car = resp.json()
    assert car["marke"] == "Honda"
    assert car["modelis"] == "Civic"
    assert "links" in car

def test_update_car_not_found(client):
    """
    Test updating a non-existent car.
    Verifies that the API responds with 404 and the correct error message.
    """
    data = {"marke": "Fake"}
    resp = client.put("/api/v1/cars/999999", json=data)
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Car not found"

def test_update_car_status_not_found(client):
    """
    Test updating the status of a non-existent car via PATCH.
    Verifies that the API responds with 404 and the correct error message.
    """
    resp = client.patch("/api/v1/cars/999999/status", json={"status": "nuomojamas"})
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Car not found"

def test_delete_car(client, ensure_place_exists):
    """
    Test creating and then deleting a car.
    Confirms the car is deleted and that the deleted car cannot be found afterwards.
    """
    data = CAR_SAMPLE.copy()
    data["numeris"] = "DELETE123"
    data["vin_kodas"] = "JH4TB2H26CC000777"
    resp = client.post("/api/v1/cars/", json=data)
    assert resp.status_code == 200
    car_id = resp.json()["automobilio_id"]
    resp = client.delete(f"/api/v1/cars/{car_id}")
    assert resp.status_code == 200
    assert resp.json()["message"] == "Car deleted successfully"
    resp = client.get(f"/api/v1/cars/{car_id}")
    assert resp.status_code == 404

def test_delete_car_not_found(client):
    """
    Test deleting a non-existent car.
    Verifies the API returns a 404 status and the correct error message.
    """
    resp = client.delete("/api/v1/cars/999999")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Car not found"
