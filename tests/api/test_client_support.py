"""
API endpoint tests for Client Support management

Author: Vytautas Petronis <vytautas.petronis@stud.viko.lt>

Description:
    Tests the /api/v1/support endpoints:
    - Creation, retrieval, and answering of support requests
    - Retrieval of all and unanswered requests
    - Edge cases: missing data, not found errors, and response structure

Usage:
    pytest tests/api/test_client_support.py
"""

import pytest

@pytest.fixture
def ensure_test_client(client):
    """
    Ensures at least one test client exists in the database.
    Creates a new client if none are present, and returns a list of clients.
    """
    klientai = client.get("/api/v1/clients/").json()
    if not klientai:
        # Sukuriam klientą, jei nėra
        klientas = {
            "vardas": "Test",
            "pavarde": "User",
            "el_pastas": "testuser@example.com",
            "telefono_nr": "+37060000000",
            "gimimo_data": "1990-01-01"
        }
        resp = client.post("/api/v1/clients/", json=klientas)
        assert resp.status_code in [200, 201]
        klientai = [resp.json()]
    return klientai

@pytest.fixture
def ensure_test_employee(client):
    """
    Ensures at least one test employee exists in the database.
    Creates a new employee if none are present, and returns a list of employees.
    """
    darbuotojai = client.get("/api/v1/employees/").json()
    if not darbuotojai:
        # Sukuriam darbuotoją, jei nėra
        darbuotojas = {
            "vardas": "Test",
            "pavarde": "Darbuotojas",
            "el_pastas": "testemployee@example.com",
            "telefono_nr": "+37061111111",
            "pareigos": "Testuotojas",
            "atlyginimas": 1000,
            "isidarbinimo_data": "2020-01-01",
            "slaptazodis": "testas"
        }
        resp = client.post("/api/v1/employees/", json=darbuotojas)
        assert resp.status_code in [200, 201]
        darbuotojai = [resp.json()]
    return darbuotojai

@pytest.fixture
def valid_ids(client, ensure_test_client, ensure_test_employee):
    """
    Returns valid client and employee IDs for use in support request tests.
    Uses test fixtures to guarantee presence in the database.
    """
    klientai = ensure_test_client
    darbuotojai = ensure_test_employee
    return {
        "kliento_id": klientai[0]["kliento_id"],
        "darbuotojo_id": darbuotojai[0]["darbuotojo_id"]
    }

@pytest.fixture
def support_sample(valid_ids):
    """
    Provides a sample payload for creating a support request.
    Uses valid test client and employee IDs from the valid_ids fixture.
    """
    return {
        "kliento_id": valid_ids["kliento_id"],
        "darbuotojo_id": valid_ids["darbuotojo_id"],
        "tema": "Testavimo klausimas",
        "pranesimas": "Testas"
    }

def test_create_support(client, support_sample):
    """
    Tests creating a new support request via POST /api/v1/support/.
    Verifies that the created request returns correct fields and links.
    """
    resp = client.post("/api/v1/support/", json=support_sample)
    assert resp.status_code == 200, resp.json()
    data = resp.json()
    assert data["tema"] == support_sample["tema"]
    assert "links" in data

def test_get_all_supports(client):
    """
    Tests retrieving all support requests via GET /api/v1/support/.
    Asserts that the response is a list and contains 'links' if not empty.
    """
    resp = client.get("/api/v1/support/")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)
    if resp.json():
        assert "links" in resp.json()[0]

def test_get_support_by_id(client, valid_ids):
    """
    Tests retrieving a support request by its ID via GET /api/v1/support/{id}.
    Asserts correctness of the returned object and presence of 'links'.
    """
    support = {
        "kliento_id": valid_ids["kliento_id"],
        "darbuotojo_id": valid_ids["darbuotojo_id"],
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
    """
    Tests fetching a support request with a non-existent ID.
    Expects a 404 status and a specific error message.
    """
    resp = client.get("/api/v1/support/9999999")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Support request not found"

def test_answer_to_support(client, valid_ids):
    """
    Tests answering a support request via PATCH /api/v1/support/{id}.
    Verifies that the answer is saved and the correct fields and links are returned.
    """
    support = {
        "kliento_id": valid_ids["kliento_id"],
        "darbuotojo_id": valid_ids["darbuotojo_id"],
        "tema": "Atsakymo testas",
        "pranesimas": "Ar veikia PATCH?"
    }
    resp = client.post("/api/v1/support/", json=support)
    assert resp.status_code == 200
    sup_id = resp.json()["uzklausos_id"]
    answer = {
        "atsakymas": "Taip, veikia.",
        "darbuotojo_id": valid_ids["darbuotojo_id"]
    }
    resp2 = client.patch(f"/api/v1/support/{sup_id}", json=answer)
    assert resp2.status_code == 200
    data = resp2.json()
    assert data["atsakymas"] == "Taip, veikia."
    assert "links" in data

def test_answer_to_support_not_found(client, valid_ids):
    """
    Tests answering a non-existent support request.
    Expects a 404 status and a 'Support request not found' error.
    """
    answer = {
        "atsakymas": "Test",
        "darbuotojo_id": valid_ids["darbuotojo_id"]
    }
    resp = client.patch("/api/v1/support/9999999", json=answer)
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Support request not found"

def test_get_unanswered_supports(client):
    """
    Tests fetching all unanswered support requests via GET /api/v1/support/unanswered.
    Asserts that the response is a list and each item (if any) has 'links'.
    """
    resp = client.get("/api/v1/support/unanswered")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)
    if resp.json():
        assert "links" in resp.json()[0]
