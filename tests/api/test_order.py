"""
API endpoint tests for Order (Užsakymų) management

Author: Vytautas Petronis <vytautas.petronis@stud.viko.lt>

Description:
    Testuoja /api/v1/orders endpointus:
    - Sukūrimas, gavimas, atnaujinimas, trynimas, kliento užsakymai
    - Edge-case (blogi ID, validacija, statusai)
    - HATEOAS nuorodų patikra, duomenų struktūra

Usage:
    pytest tests/api/test_order.py
"""

import pytest

ORDER_SAMPLE = {
    "kliento_id": 1,
    "automobilio_id": 1,
    "darbuotojo_id": 1,
    "nuomos_data": "2024-06-01",
    "grazinimo_data": "2024-06-10",
    "paemimo_vietos_id": 1,
    "grazinimo_vietos_id": 1,
    "bendra_kaina": 350,
    "uzsakymo_busena": "patvirtintas",
    "turi_papildomas_paslaugas": False
}


@pytest.fixture(scope="module")
def created_order_id(client):
    """
    Sukuria testinį užsakymą ir grąžina jo ID.
    Po testų jį ištrina.
    """
    resp = client.post("/api/v1/orders/", json=ORDER_SAMPLE)
    assert resp.status_code == 200
    order = resp.json()
    yield order["uzsakymo_id"]
    client.delete(f"/api/v1/orders/{order['uzsakymo_id']}")

def test_create_order(client):
    data = ORDER_SAMPLE.copy()
    data["nuomos_data"] = "2024-07-01"
    data["grazinimo_data"] = "2024-07-03"
    resp = client.post("/api/v1/orders/", json=data)
    assert resp.status_code == 200
    order = resp.json()
    assert "uzsakymo_id" in order
    assert order["uzsakymo_busena"] == data["uzsakymo_busena"]
    assert "links" in order
    client.delete(f"/api/v1/orders/{order['uzsakymo_id']}")

def test_create_order_missing_required(client):
    """Bando sukurti užsakymą be automobilio_id (tikrina validaciją)."""
    data = ORDER_SAMPLE.copy()
    data.pop("automobilio_id")
    resp = client.post("/api/v1/orders/", json=data)
    assert resp.status_code in (400, 422)  # Priklausomai nuo validacijos

def test_get_all_orders(client, created_order_id):
    """Gauna visų užsakymų sąrašą (turi būti bent vienas)."""
    resp = client.get("/api/v1/orders/")
    assert resp.status_code == 200
    orders = resp.json()
    assert isinstance(orders, list)
    assert any(o["uzsakymo_id"] == created_order_id for o in orders)
    assert all("links" in o for o in orders)

def test_get_order_by_id(client, created_order_id):
    """Grąžina užsakymą pagal ID (sėkmingas atvejis)."""
    resp = client.get(f"/api/v1/orders/{created_order_id}")
    assert resp.status_code == 200
    order = resp.json()
    assert order["uzsakymo_id"] == created_order_id
    assert "links" in order
    assert order["kliento_id"] == ORDER_SAMPLE["kliento_id"]

def test_get_order_not_found(client):
    """Bando gauti neegzistuojantį užsakymą."""
    resp = client.get("/api/v1/orders/999999")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Order not found"

def test_update_order(client, created_order_id):
    update_data = {
        "uzsakymo_busena": "atšauktas",
        "grazinimo_data": "2024-07-20",
        "turi_papildomas_paslaugas": True
    }
    resp = client.put(f"/api/v1/orders/{created_order_id}", json=update_data)
    assert resp.status_code == 200
    order = resp.json()
    assert order["uzsakymo_busena"] == "atšauktas"
    assert order["turi_papildomas_paslaugas"] == True
    assert "links" in order

def test_update_order_not_found(client):
    data = {"uzsakymo_busena": "test"}
    resp = client.put("/api/v1/orders/999999", json=data)
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Order not found"

def test_delete_order(client):
    data = ORDER_SAMPLE.copy()
    data["nuomos_data"] = "2024-08-01"
    data["grazinimo_data"] = "2024-08-10"
    resp = client.post("/api/v1/orders/", json=data)
    assert resp.status_code == 200
    order_id = resp.json()["uzsakymo_id"]
    resp = client.delete(f"/api/v1/orders/{order_id}")
    assert resp.status_code == 200
    assert resp.json()["ok"] is True
    resp = client.get(f"/api/v1/orders/{order_id}")
    assert resp.status_code == 404


def test_delete_order_not_found(client):
    """Bando ištrinti neegzistuojantį užsakymą."""
    resp = client.delete("/api/v1/orders/999999")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Order not found"

def test_get_orders_for_client(client):
    """Gauna visus užsakymus pagal kliento_id."""
    client_id = ORDER_SAMPLE["kliento_id"]
    resp = client.get(f"/api/v1/orders/by-client/{client_id}")
    assert resp.status_code == 200
    orders = resp.json()
    assert isinstance(orders, list)
    if orders:
        assert "links" in orders[0]
