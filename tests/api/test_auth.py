"""
API Authentication endpoint tests

Author: Vytautas Petronis <vytautas.petronis@stud.viko.lt>

Description:
    Unit and integration tests for authentication endpoints:
    - /login
    - /register
    - /me (profile)
    - /change-password
    - /logout

    Covers success, failure and edge-cases, tests JWT logic, and endpoint validation.

Requirements:
    - conftest.py fixture `client`
    - Test DB reset or rollback after each test (recommended)
    - Test user created before login tests

Usage:
    pytest tests/api/test_auth.py

"""

import pytest

# Jei naudoji "client" fixture iš conftest.py
from fastapi.testclient import TestClient

# Dummy credentials for test user
TEST_USER = {
    "vardas": "Testas",
    "pavarde": "Testavicius",
    "el_pastas": "test.auth@viko.lt",
    "slaptazodis": "Slaptas123!",
    "telefono_nr": "+37061234567",
    "pareigos": "Testuotojas",
    "atlyginimas": 1000,
    "isidarbinimo_data": "2024-01-01"
}


@pytest.fixture(scope="module")
def create_test_user(client: TestClient):
    """Sukuria testinį userį registracijos endpointu (one-time, module-scope)."""
    resp = client.post("/api/v1/register", json=TEST_USER)
    # Gali būti 400 jei user jau egzistuoja – svarbu, kad egzistuotų!
    assert resp.status_code in (200, 400)
    yield
    # Po testų – galima userį ištrinti iš DB, jei reikia.


def test_register_new_user(client):
    """Testuoja sėkmingą registraciją (unikalus el. paštas)."""
    data = TEST_USER.copy()
    # Sugeneruojam unikalų email, pvz. su atsitiktiniu arba timestamp
    import time
    unique_email = f"unikalus_{int(time.time())}@viko.lt"
    data["el_pastas"] = unique_email
    resp = client.post("/api/v1/register", json=data)
    print(resp.status_code)
    print(resp.json())
    assert resp.status_code == 200


def test_register_duplicate_user(client, create_test_user):
    """Testuoja dublikatų el. pašto registracijos klaidą."""
    resp = client.post("/api/v1/register", json=TEST_USER)
    assert resp.status_code == 400
    assert resp.json()["detail"] == "Employee with this email already exists"


def test_login_success(client, create_test_user):
    """Sėkmingas prisijungimas – grąžina JWT tokeną."""
    resp = client.post("/api/v1/login", json={
        "el_pastas": TEST_USER["el_pastas"],
        "slaptazodis": TEST_USER["slaptazodis"]
    })
    assert resp.status_code == 200
    res_json = resp.json()
    assert "access_token" in res_json
    assert len(res_json["access_token"]) > 10


def test_login_wrong_password(client):
    """Blogas slaptažodis – turi būti 401 klaida."""
    resp = client.post("/api/v1/login", json={
        "el_pastas": TEST_USER["el_pastas"],
        "slaptazodis": "netinkamasSlaptazodis"
    })
    assert resp.status_code == 401
    assert resp.json()["detail"] == "Invalid login credentials"


def test_login_nonexistent_user(client):
    """Neegzistuojantis vartotojas – 401 klaida."""
    resp = client.post("/api/v1/login", json={
        "el_pastas": "nesamas@viko.lt",
        "slaptazodis": "betkas"
    })
    assert resp.status_code == 401
    assert resp.json()["detail"] == "Invalid login credentials"


def test_me_endpoint_success(client, create_test_user):
    """Grąžina prisijungusio vartotojo profilį su JWT tokenu."""
    # Pirma prisijungiame
    resp = client.post("/api/v1/login", json={
        "el_pastas": TEST_USER["el_pastas"],
        "slaptazodis": TEST_USER["slaptazodis"]
    })
    token = resp.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    resp = client.get("/api/v1/me", headers=headers)
    assert resp.status_code == 200
    profile = resp.json()
    assert profile["el_pastas"] == TEST_USER["el_pastas"]


def test_me_endpoint_unauthorized(client):
    """Be tokeno turi mesti 401 klaidą."""
    resp = client.get("/api/v1/me")
    assert resp.status_code == 403 or resp.status_code == 401


def test_change_password_success(client, create_test_user):
    """Keičia slaptažodį – patikrina, kad naujas slaptažodis veikia loginui."""
    # Prisijungiam ir gaunam JWT
    resp = client.post("/api/v1/login", json={
        "el_pastas": TEST_USER["el_pastas"],
        "slaptazodis": TEST_USER["slaptazodis"]
    })
    token = resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    new_pw = "NaujasSlaptazodis123!"

    resp = client.post("/api/v1/change-password", json={
        "senas_slaptazodis": TEST_USER["slaptazodis"],
        "naujas_slaptazodis": new_pw
    }, headers=headers)
    assert resp.status_code == 200
    assert resp.json()["message"] == "Password updated successfully"

    # Patikrinam login su nauju slaptažodžiu
    resp = client.post("/api/v1/login", json={
        "el_pastas": TEST_USER["el_pastas"],
        "slaptazodis": new_pw
    })
    assert resp.status_code == 200
    assert "access_token" in resp.json()

    # (Optional) Grąžinam atgal seną slaptažodį, kad kiti testai nenulūžtų
    resp = client.post("/api/v1/change-password", json={
        "senas_slaptazodis": new_pw,
        "naujas_slaptazodis": TEST_USER["slaptazodis"]
    }, headers={"Authorization": f"Bearer {resp.json()['access_token']}"})
    # Gali nesuveikti dėl tokeno, praleisti


def test_change_password_wrong_old_pw(client, create_test_user):
    """Bandymas keisti slaptažodį su neteisingu senu slaptažodžiu."""
    # Prisijungiam ir gaunam JWT
    resp = client.post("/api/v1/login", json={
        "el_pastas": TEST_USER["el_pastas"],
        "slaptazodis": TEST_USER["slaptazodis"]
    })
    token = resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    resp = client.post("/api/v1/change-password", json={
        "senas_slaptazodis": "blogas123",
        "naujas_slaptazodis": "NaujasSlaptazodis456!"
    }, headers=headers)
    assert resp.status_code == 400
    assert resp.json()["detail"] == "Wrong current password"


def test_logout(client):
    """Logout endpointas veikia (nors tai tik placeholder'is, turi grąžinti 200)."""
    resp = client.post("/api/v1/logout")
    assert resp.status_code == 200
    assert resp.json()["message"] == "Successfully logged out"

