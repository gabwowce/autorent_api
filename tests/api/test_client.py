"""
API endpoint tests for Client management

Author: Vytautas Petronis <vytautas.petronis@stud.viko.lt>

Description:
    Integration tests for /api/v1/clients endpointus:
    - Sukūrimas, gavimas, trynimas, užsakymų sąrašas
    - Sėkmingi ir nesėkmingi (edge) atvejai
    - HATEOAS nuorodų patikra, duomenų validacija

Usage:
    pytest tests/api/test_client.py
"""

import pytest

CLIENT_SAMPLE = {
    "vardas": "Testas",
    "pavarde": "Kliūzas",
    "el_pastas": "client.test@viko.lt",
    "telefono_nr": "+37060000000",
    "gimimo_data": "1995-01-01",
    "registracijos_data": "2024-06-02T00:00:00",
    "bonus_taskai": 0
}

@pytest.fixture(scope="module")
def created_client_id(client):
    """Sukuria klientą ir grąžina jo ID, ištrina po testų."""
    resp = client.post("/api/v1/clients/", json=CLIENT_SAMPLE)
    assert resp.status_code == 200
    client_obj = resp.json()
    yield client_obj["kliento_id"]
    # Ištrynimas
    client.delete(f"/api/v1/clients/{client_obj['kliento_id']}")


def test_create_client(client):
    """Sukuria naują klientą (happy path)."""
    data = CLIENT_SAMPLE.copy()
    data["el_pastas"] = "client.unique@viko.lt"
    resp = client.post("/api/v1/clients/", json=data)
    print("DEBUG:", resp.status_code, resp.json())
    assert resp.status_code == 200
    obj = resp.json()
    assert obj["el_pastas"] == data["el_pastas"]
    assert "links" in obj
    # Clean up
    client.delete(f"/api/v1/clients/{obj['kliento_id']}")


def test_create_client_missing_required(client):
    """Bando sukurti klientą be privalomo el_pastas (tikrina validaciją)."""
    data = CLIENT_SAMPLE.copy()
    data.pop("el_pastas")
    resp = client.post("/api/v1/clients/", json=data)
    assert resp.status_code in (400, 422)  # FastAPI dažniausiai 422


def test_get_all_clients(client, created_client_id):
    """Grąžina visų klientų sąrašą (turi būti bent vienas)."""
    resp = client.get("/api/v1/clients/")
    assert resp.status_code == 200
    clients = resp.json()
    assert isinstance(clients, list)
    assert any(c["kliento_id"] == created_client_id for c in clients)
    assert all("links" in c for c in clients)


def test_get_client_by_id(client, created_client_id):
    """Grąžina klientą pagal ID (sėkmingas atvejis)."""
    resp = client.get(f"/api/v1/clients/{created_client_id}")
    assert resp.status_code == 200
    cl = resp.json()
    assert cl["kliento_id"] == created_client_id
    assert "links" in cl
    assert cl["vardas"] == CLIENT_SAMPLE["vardas"]


def test_get_client_not_found(client):
    """Klaida, jei klientas neegzistuoja."""
    resp = client.get("/api/v1/clients/999999")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Client not found"


def test_delete_client(client):
    """Sukuria ir ištrina klientą."""
    data = CLIENT_SAMPLE.copy()
    data["el_pastas"] = "client.delete@viko.lt"
    resp = client.post("/api/v1/clients/", json=data)
    assert resp.status_code == 200
    cid = resp.json()["kliento_id"]
    resp = client.delete(f"/api/v1/clients/{cid}")
    assert resp.status_code == 200
    assert resp.json()["ok"] is True
    # Patikrina, ar tikrai ištrinta
    resp = client.get(f"/api/v1/clients/{cid}")
    assert resp.status_code == 404


def test_delete_client_not_found(client):
    """Bando ištrinti neegzistuojantį klientą."""
    resp = client.delete("/api/v1/clients/999999")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Client not found"