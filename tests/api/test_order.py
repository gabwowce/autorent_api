"""
API endpoint tests for Order management.

Author: Vytautas Petronis <vytautas.petronis@stud.viko.lt>

Description:
    This module contains integration tests for the /api/v1/orders endpoints of the Car Rental RESTful API.
    The tests cover order creation, retrieval, update, deletion, and client-specific orders.
    Edge-cases, validation, HATEOAS link presence, and response data structures are also verified.

Usage:
    pytest tests/api/test_order.py
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from uuid import uuid4
from app.api.deps import get_db
from app.models import Location

client = TestClient(app)

@pytest.fixture(scope="module")
def ensure_place_exists():
    """
    Ensures that a location with ID=1 exists in the database for test setup.
    If not present, creates the location.
    """
    db = next(get_db())
    vieta = db.query(Location).filter_by(vietos_id=1).first()
    if not vieta:
        vieta = Location(vietos_id=1, pavadinimas="Testo vieta", adresas="Test gatvė 1", miestas="Vilnius")
        db.add(vieta)
        db.commit()
    yield vieta

@pytest.fixture
def prepared_order(ensure_place_exists):
    """
    Prepares and returns all required IDs for an order:
    - Creates a test location, car, employee, and client via the API,
      then creates an order linking them all together.
    Returns a dict with created order, client, car, and employee IDs.
    """
    location_resp = client.post("/api/v1/locations/", json={
        "pavadinimas": "Vilnius Centras",
        "adresas": "Gedimino pr. 1",
        "miestas": "Vilnius"
    })
    location_id = 1
    if location_resp.status_code in [200, 201]:
        location_id = location_resp.json().get("vietos_id", 1)

    car_resp = client.post("/api/v1/cars/", json={
        "marke": "Toyota",
        "modelis": "Corolla",
        "metai": 2021,
        "numeris": f"ABC{uuid4().hex[:3].upper()}",
        "vin_kodas": uuid4().hex[:16].upper(),
        "spalva": "Juoda",
        "kebulo_tipas": "Sedanas",
        "pavarų_deze": "automatinė",
        "variklio_turis": 1.6,
        "galia_kw": 97,
        "kuro_tipas": "benzinas",
        "rida": 15000,
        "sedimos_vietos": 5,
        "klimato_kontrole": True,
        "navigacija": True,
        "kaina_parai": 40.00,
        "automobilio_statusas": "laisvas",
        "technikines_galiojimas": "2025-12-31",
        "dabartine_vieta_id": location_id,
        "pastabos": "Testinis auto"
    })
    car_id = car_resp.json().get("automobilio_id") or car_resp.json().get("id")
    assert car_id is not None

    emp_resp = client.post("/api/v1/employees/", json={
        "vardas": "Testas",
        "pavarde": "Darbuotojas",
        "el_pastas": f"darbuotojas{uuid4().hex[:6]}@viko.lt",
        "slaptazodis": "slaptas123!",
        "telefono_nr": "+37060000002",
        "pareigos": "Administratorius",
        "atlyginimas": 1800.00,
        "isidarbinimo_data": "2023-01-01"
    })
    emp_id = emp_resp.json().get("darbuotojo_id") or emp_resp.json().get("id")
    assert emp_id is not None

    el_pastas = f"testas{uuid4().hex[:8]}@viko.lt"
    client_resp = client.post("/api/v1/clients/", json={
        "vardas": "Testas",
        "pavarde": "Testavičius",
        "el_pastas": el_pastas,
        "telefono_nr": "+37060000000",
        "slaptazodis": "labaiSaugus123!",
        "gimimo_data": "2000-01-01",
        "registracijos_data": "2024-06-01",
        "bonus_taskai": 0
    })
    resp_json = client_resp.json()
    client_id = (
        resp_json.get("kliento_id")
        or resp_json.get("client_id")
        or resp_json.get("id")
        or (resp_json.get("data", {}).get("kliento_id") if resp_json.get("data") else None)
    )
    assert client_id is not None

    order_body = {
        "kliento_id": client_id,
        "automobilio_id": car_id,
        "darbuotojo_id": emp_id,
        "nuomos_data": "2024-06-01",
        "grazinimo_data": "2024-06-10",
        "paemimo_vietos_id": 1,
        "grazinimo_vietos_id": 1,
        "bendra_kaina": 100.0,
        "uzsakymo_busena": "patvirtinta",
        "turi_papildomas_paslaugas": False
    }
    order_resp = client.post("/api/v1/orders/", json=order_body)
    order_id = order_resp.json().get("uzsakymo_id") or order_resp.json().get("order_id")
    assert order_id is not None
    return {
        "order_id": order_id,
        "client_id": client_id,
        "car_id": car_id,
        "emp_id": emp_id
    }

def test_create_order(prepared_order):
    """
    Tests successful creation of an order via the API.
    Verifies status code, fields in the response, and cleans up by deleting.
    """
    data = {
        "kliento_id": prepared_order["client_id"],
        "automobilio_id": prepared_order["car_id"],
        "darbuotojo_id": prepared_order["emp_id"],
        "nuomos_data": "2024-07-01",
        "grazinimo_data": "2024-07-03",
        "paemimo_vietos_id": 1,
        "grazinimo_vietos_id": 1,
        "bendra_kaina": 350,
        "uzsakymo_busena": "patvirtinta",
        "turi_papildomas_paslaugas": False
    }
    resp = client.post("/api/v1/orders/", json=data)
    assert resp.status_code == 200
    order = resp.json()
    assert "uzsakymo_id" in order
    assert order["uzsakymo_busena"] == data["uzsakymo_busena"]
    assert "links" in order
    client.delete(f"/api/v1/orders/{order['uzsakymo_id']}")

def test_create_order_missing_required(prepared_order):
    """
    Tests order creation with missing required fields (car ID) to ensure validation fails.
    Expects HTTP 400 or 422.
    """
    data = {
    "kliento_id": prepared_order["client_id"],
    "darbuotojo_id": prepared_order["emp_id"],
    "nuomos_data": "2024-07-01",
    "grazinimo_data": "2024-07-03",
    "paemimo_vietos_id": 1,
    "grazinimo_vietos_id": 1,
    "bendra_kaina": 350,
    "uzsakymo_busena": "patvirtinta",
    "turi_papildomas_paslaugas": False
    }
    resp = client.post("/api/v1/orders/", json=data)
    assert resp.status_code in (400, 422)  # Priklausomai nuo validacijos

def test_get_all_orders(prepared_order):
    """
    Tests fetching the list of all orders.
    Checks that the list contains the prepared order and that every order has HATEOAS links.
    """
    resp = client.get("/api/v1/orders/")
    assert resp.status_code == 200
    orders = resp.json()
    assert isinstance(orders, list)
    assert any(o["uzsakymo_id"] == prepared_order["order_id"] for o in orders)
    assert all("links" in o for o in orders)

def test_get_order_by_id(prepared_order):
    """
    Tests retrieving an order by its ID.
    Verifies response fields and HATEOAS links are present.
    """
    resp = client.get(f"/api/v1/orders/{prepared_order['order_id']}")
    assert resp.status_code == 200
    order = resp.json()
    assert order["uzsakymo_id"] == prepared_order["order_id"]
    assert "links" in order
    assert order["kliento_id"] == prepared_order["client_id"]

def test_get_order_not_found(client):
    """
    Tests retrieving a non-existent order.
    Expects HTTP 404 and correct error message.
    """
    resp = client.get("/api/v1/orders/999999")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Order not found"

def test_update_order(prepared_order):
    """
    Tests updating an order's status and fields via the API.
    Verifies updated values and link presence.
    """
    update_data = {
        "uzsakymo_busena": "atšauktas",
        "grazinimo_data": "2024-07-20",
        "turi_papildomas_paslaugas": True
    }
    resp = client.put(f"/api/v1/orders/{prepared_order['order_id']}", json=update_data)
    assert resp.status_code == 200
    order = resp.json()
    assert order["uzsakymo_busena"] == "atšauktas"
    assert order["turi_papildomas_paslaugas"] == True
    assert "links" in order

def test_update_order_not_found(client):
    """
    Tests updating a non-existent order.
    Expects HTTP 404 and correct error message.
    """
    data = {"uzsakymo_busena": "test"}
    resp = client.put("/api/v1/orders/999999", json=data)
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Order not found"

def test_delete_order(prepared_order):
    """
    Tests creating and then deleting an order via the API.
    Verifies successful deletion and that the order no longer exists.
    """
    data = {
    "kliento_id": prepared_order["client_id"],
    "automobilio_id": prepared_order["car_id"],
    "darbuotojo_id": prepared_order["emp_id"],
    "nuomos_data": "2024-08-01",
    "grazinimo_data": "2024-08-10",
    "paemimo_vietos_id": 1,
    "grazinimo_vietos_id": 1,
    "bendra_kaina": 350,
    "uzsakymo_busena": "patvirtinta",
    "turi_papildomas_paslaugas": False
    }
    resp = client.post("/api/v1/orders/", json=data)
    assert resp.status_code == 200
    order_id = resp.json()["uzsakymo_id"]
    resp = client.delete(f"/api/v1/orders/{order_id}")
    assert resp.status_code == 200
    assert resp.json()["ok"] is True
    resp = client.get(f"/api/v1/orders/{order_id}")
    assert resp.status_code == 404

def test_delete_order_not_found(client):
    """
    Tests deleting a non-existent order.
    Expects HTTP 404 and correct error message.
    """
    resp = client.delete("/api/v1/orders/999999")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Order not found"

def test_get_orders_for_client(prepared_order):
    """
    Tests retrieving all orders for a specific client via client_id.
    Checks response list and that HATEOAS links are present if there are results.
    """
    client_id = prepared_order["client_id"]
    resp = client.get(f"/api/v1/orders/by-client/{client_id}")

    assert resp.status_code == 200
    orders = resp.json()
    assert isinstance(orders, list)
    if orders:
        assert "links" in orders[0]
