"""
API endpoint tests for Client Support management

Author: Vytautas Petronis <vytautas.petronis@stud.viko.lt>

Testuoja /api/v1/support endpointus:

Naudojimas:
    pytest tests/api/test_client_support.py
"""

import pytest

# Privalo būti galiojantys ID tavo duomenų bazėje!
EXISTING_CLIENT_ID = 1
EXISTING_EMPLOYEE_ID = 1

@pytest.fixture
def support_sample():
    return {
        "kliento_id": EXISTING_CLIENT_ID,
        "darbuotojo_id": EXISTING_EMPLOYEE_ID,
        "tema": "Testavimo klausimas",
        "pranesimas": "Testas"
    }

def test_create_support(client, support_sample):
    resp = client.post("/api/v1/support/", json=support_sample)
    assert resp.status_code == 200, resp.json()
    data = resp.json()
    assert data["tema"] == support_sample["tema"]
    assert "links" in data
    # cleanup: delete (jei būtų endpointas /support/{id} su DELETE)

def test_get_all_supports(client):
    resp = client.get("/api/v1/support/")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)
    if resp.json():
        assert "links" in resp.json()[0]

def test_get_support_by_id(client):
    # Sukuriam supportą, tada gaunam pagal id
    support = {
        "kliento_id": EXISTING_CLIENT_ID,
        "darbuotojo_id": EXISTING_EMPLOYEE_ID,
        "tema": "GET testas",
        "pranesimas": "GET pagal id"
    }
    resp = client.post("/api/v1/support/", json=support)
    assert resp.status_code == 200
    sup_id = resp.json()["uzklausos_id"]
    resp2 = client.get(f"/api/v1/support/{sup_id}")
    assert resp2.status_code == 200
    data = resp2.json()
    assert data["uzklausos_id"] == sup_id
    assert data["tema"] == "GET testas"
    assert "links" in data

def test_get_support_not_found(client):
    resp = client.get("/api/v1/support/9999999")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Support request not found"

def test_answer_to_support(client):
    # Sukuriam support, tada PATCHinam atsakymą
    support = {
        "kliento_id": EXISTING_CLIENT_ID,
        "darbuotojo_id": EXISTING_EMPLOYEE_ID,
        "tema": "Atsakymo testas",
        "pranesimas": "Ar veikia PATCH?"
    }
    resp = client.post("/api/v1/support/", json=support)
    assert resp.status_code == 200
    sup_id = resp.json()["uzklausos_id"]
    answer = {
        "atsakymas": "Taip, veikia.",
        "darbuotojo_id": EXISTING_EMPLOYEE_ID
    }
    resp2 = client.patch(f"/api/v1/support/{sup_id}", json=answer)
    assert resp2.status_code == 200
    data = resp2.json()
    assert data["atsakymas"] == "Taip, veikia."
    assert "links" in data

def test_answer_to_support_not_found(client):
    answer = {
        "atsakymas": "Test",
        "darbuotojo_id": EXISTING_EMPLOYEE_ID
    }
    resp = client.patch("/api/v1/support/9999999", json=answer)
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Support request not found"

def test_get_unanswered_supports(client):
    resp = client.get("/api/v1/support/unanswered")
    print(resp.json())   # <--- ČIA
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)
    if resp.json():
        assert "links" in resp.json()[0]
