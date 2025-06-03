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

CAR_SAMPLE = {
    "marke": "Toyota",
    "modelis": "Corolla",
    "metai": 2022,
    "numeris": "TEST123",
    "vin_kodas": "JH4TB2H26CC000000",
    "spalva": "Mėlyna",
    "kebulo_tipas": "Sedanas",
    "pavarų_deze": "Automatinė",
    "variklio_turis": 1.8,
    "galia_kw": 103,
    "kuro_tipas": "Benzinas",
    "rida": 10000,
    "sedimos_vietos": 5,
    "klimato_kontrole": True,
    "navigacija": False,
    "kaina_parai": 50.0,
    "automobilio_statusas": "laisvas",
    "technikines_galiojimas": "2025-12-31",
    "dabartine_vieta_id": 1,  # ne None, turi būti int
    "pastabos": "Test car"
}

@pytest.fixture(scope="module")
def created_car_id(client):
    """Create a car and yield its ID (cleanup can be added if needed)."""
    resp = client.post("/api/v1/cars/", json=CAR_SAMPLE)
    assert resp.status_code == 200
    car = resp.json()
    yield car["automobilio_id"]
    # Optionally, delete after tests:
    client.delete(f"/api/v1/cars/{car['automobilio_id']}")

def test_create_car(client):
    """Test car creation (happy path)."""
    car_data = CAR_SAMPLE.copy()
    car_data["numeris"] = "TEST999"
    car_data["vin_kodas"] = "JH4TB2H26CC000999"
    resp = client.post("/api/v1/cars/", json=car_data)
    assert resp.status_code == 200
    res = resp.json()
    assert res["marke"] == car_data["marke"]
    assert "automobilio_id" in res
    assert "links" in res
    # Clean up
    client.delete(f"/api/v1/cars/{res['automobilio_id']}")

def test_get_all_cars(client, created_car_id):
    """Test retrieving all cars (should return at least one)."""
    resp = client.get("/api/v1/cars/")
    assert resp.status_code == 200
    cars = resp.json()
    assert isinstance(cars, list)
    assert any(c["automobilio_id"] == created_car_id for c in cars)
    # HATEOAS link check
    assert all("links" in c for c in cars)

def test_get_car_by_id(client, created_car_id):
    """Test retrieving a car by ID (positive case)."""
    resp = client.get(f"/api/v1/cars/{created_car_id}")
    assert resp.status_code == 200
    car = resp.json()
    assert car["automobilio_id"] == created_car_id
    assert "links" in car
    # Check some fields
    assert car["marke"] == CAR_SAMPLE["marke"]

def test_get_car_not_found(client):
    """Try getting a car that does not exist."""
    resp = client.get("/api/v1/cars/999999")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Car not found"

def test_update_car(client, created_car_id):
    """Test car update (PUT)."""
    update_data = {"marke": "Honda", "modelis": "Civic"}
    resp = client.put(f"/api/v1/cars/{created_car_id}", json=update_data)
    assert resp.status_code == 200
    car = resp.json()
    assert car["marke"] == "Honda"
    assert car["modelis"] == "Civic"
    assert "links" in car

def test_update_car_not_found(client):
    """Try updating a non-existent car."""
    data = {"marke": "Fake"}
    resp = client.put("/api/v1/cars/999999", json=data)
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Car not found"

def test_update_car_status_not_found(client):
    """Try updating status for a non-existent car."""
    resp = client.patch("/api/v1/cars/999999/status", json={"status": "nuomojamas"})
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Car not found"

def test_delete_car(client):
    """Create and then delete a car (DELETE)."""
    data = CAR_SAMPLE.copy()
    data["numeris"] = "DELETE123"
    data["vin_kodas"] = "JH4TB2H26CC000777"
    resp = client.post("/api/v1/cars/", json=data)
    assert resp.status_code == 200
    car_id = resp.json()["automobilio_id"]
    resp = client.delete(f"/api/v1/cars/{car_id}")
    assert resp.status_code == 200
    assert resp.json()["message"] == "Car deleted successfully"
    # Ensure it really is gone
    resp = client.get(f"/api/v1/cars/{car_id}")
    assert resp.status_code == 404

def test_delete_car_not_found(client):
    """Bandymas ištrinti neegzistuojantį automobilį."""
    resp = client.delete("/api/v1/cars/999999")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Car not found"
