"""
Integration tests for Reservation API endpoints.

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
from uuid import uuid4
from app.api.deps import get_db
from app.models.location import Location

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def ensure_pristatymo_vieta():
    """
    Ensures that a test Location (with id=1) exists in the database before running any reservation tests.
    If the location does not exist, it creates one. This fixture is applied automatically for all tests in this module.
    """
    db = next(get_db())
    vieta = db.query(Location).filter_by(vietos_id=1).first()
    if not vieta:
        vieta = Location(
            vietos_id=1,
            pavadinimas="Testo vieta",
            adresas="Test gatvė 1",
            miestas="Vilnius"
        )
        db.add(vieta)
        db.commit()
    yield vieta

@pytest.fixture
def example_reservation_data():
    """
    Creates and returns example reservation data required for testing:
    - Ensures a test client exists (and creates a new one if needed)
    - Ensures a test car exists (and creates a new one if needed)
    - Returns a dictionary with valid fields to create a reservation
    """
    # Sukuriam lokaciją
    vietos_id = 1  # nes fixture užtikrina, kad egzistuoja

    # Sukuriam klientą
    cl_resp = client.post("/api/v1/clients/", json={
        "vardas": "Testas",
        "pavarde": "Rezervavicius",
        "el_pastas": f"rez{uuid4().hex[:8]}@test.lt",
        "telefono_nr": "+37060000011",
        "slaptazodis": "SlaptasRez123!",
        "gimimo_data": "2000-01-01",
        "registracijos_data": "2024-06-01",
        "bonus_taskai": 0
    })
    kliento_id = cl_resp.json().get("kliento_id") or cl_resp.json().get("id")

    # Sukuriam automobilį
    car_resp = client.post("/api/v1/cars/", json={
        "marke": "Toyota",
        "modelis": "Aygo",
        "metai": 2022,
        "numeris": f"RES{uuid4().hex[:3].upper()}",
        "vin_kodas": uuid4().hex[:16].upper(),
        "spalva": "Raudona",
        "kebulo_tipas": "Hečbekas",
        "pavarų_deze": "mechaninė",
        "variklio_turis": 1.0,
        "galia_kw": 53,
        "kuro_tipas": "benzinas",
        "rida": 10000,
        "sedimos_vietos": 4,
        "klimato_kontrole": False,
        "navigacija": False,
        "kaina_parai": 29.99,
        "automobilio_statusas": "laisvas",
        "technikines_galiojimas": "2025-12-31",
        "dabartine_vieta_id": vietos_id,
        "pastabos": "Rez test"
    })
    automobilio_id = car_resp.json().get("automobilio_id") or car_resp.json().get("id")

    return {
        "kliento_id": kliento_id,
        "automobilio_id": automobilio_id,
        "rezervacijos_pradzia": "2024-06-01",
        "rezervacijos_pabaiga": "2024-06-03",
        "busena": "aktyvi"
    }

def test_create_reservation(example_reservation_data):
    """
    Tests successful reservation creation via the POST /api/v1/reservations/ endpoint.
    Asserts that the response status code is 200 or 201 and that the returned reservation data matches the request.
    """
    response = client.post("/api/v1/reservations/", json=example_reservation_data)
    assert response.status_code in [200, 201]
    data = response.json()
    assert "rezervacijos_id" in data
    assert data["kliento_id"] == example_reservation_data["kliento_id"]
    assert data["automobilio_id"] == example_reservation_data["automobilio_id"]

def test_get_all_reservations():
    """
    Tests retrieving all reservations via the GET /api/v1/reservations/ endpoint.
    Asserts that the response status code is 200 and that the response contains a list of reservations.
    """
    response = client.get("/api/v1/reservations/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_reservation_by_id(example_reservation_data):
    """
    Tests retrieving a specific reservation by its ID using GET /api/v1/reservations/{id}.
    Asserts that the correct reservation is returned.
    """
    res_resp = client.post("/api/v1/reservations/", json=example_reservation_data)
    res_id = res_resp.json()["rezervacijos_id"]
    get_resp = client.get(f"/api/v1/reservations/{res_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["rezervacijos_id"] == res_id

def test_delete_reservation(example_reservation_data):
    """
    Tests deleting a reservation via DELETE /api/v1/reservations/{id}.
    Asserts that the reservation is successfully deleted and is no longer present in the list of all reservations.
    """
    res_resp = client.post("/api/v1/reservations/", json=example_reservation_data)
    res_id = res_resp.json()["rezervacijos_id"]
    del_resp = client.delete(f"/api/v1/reservations/{res_id}")
    assert del_resp.status_code in [200, 204]
    get_all = client.get("/api/v1/reservations/").json()
    ids = [r["rezervacijos_id"] for r in get_all]
    assert res_id not in ids