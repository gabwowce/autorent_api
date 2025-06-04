"""
API Authentication endpoint tests

Author: Vytautas Petronis <vytautas.petronis@stud.viko.lt>

This test suite contains unit and integration tests for user authentication API endpoints.

Tests cover:
    - User registration (/register)
    - User login (/login)
    - Retrieving current user profile (/me)
    - Changing user password (/change-password)
    - Logging out (/logout)
    - Various error and edge cases, including duplicate users, wrong credentials, and JWT logic.

Usage:
    pytest tests/api/test_auth.py

Dependencies:
    - Requires `client` fixture from conftest.py (FastAPI TestClient)
    - It is recommended to reset or rollback the test database after each test.
"""


import pytest
from fastapi.testclient import TestClient

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
    """
    Creates a test user using the registration endpoint if it does not exist yet.
    Ensures the test user is available for authentication-related tests.
    """
    resp = client.post("/api/v1/register", json=TEST_USER)
    assert resp.status_code in (200, 400)
    yield


def test_register_new_user(client):
    """
    Tests successful user registration using a unique email.
    Checks that a new user can be registered and receives a 200 status.
    """
    data = TEST_USER.copy()
    import time
    unique_email = f"unikalus_{int(time.time())}@viko.lt"
    data["el_pastas"] = unique_email
    resp = client.post("/api/v1/register", json=data)
    print(resp.status_code)
    print(resp.json())
    assert resp.status_code == 200


def test_register_duplicate_user(client, create_test_user):
    """
    Tests registration with an existing email address.
    Expects a 400 error and a specific error message about duplicate user.
    """
    resp = client.post("/api/v1/register", json=TEST_USER)
    assert resp.status_code == 400
    assert resp.json()["detail"] == "Employee with this email already exists"


def test_login_success(client, create_test_user):
    """
    Tests successful user login.
    Ensures a valid JWT access token is returned upon correct credentials.
    """
    resp = client.post("/api/v1/login", json={
        "el_pastas": TEST_USER["el_pastas"],
        "slaptazodis": TEST_USER["slaptazodis"]
    })
    assert resp.status_code == 200
    res_json = resp.json()
    assert "access_token" in res_json
    assert len(res_json["access_token"]) > 10


def test_login_wrong_password(client):
    """
    Tests login with a wrong password for an existing user.
    Expects a 401 error and an invalid credentials message.
    """
    resp = client.post("/api/v1/login", json={
        "el_pastas": TEST_USER["el_pastas"],
        "slaptazodis": "netinkamasSlaptazodis"
    })
    assert resp.status_code == 401
    assert resp.json()["detail"] == "Invalid login credentials"


def test_login_nonexistent_user(client):
    """
    Tests login with an email that does not exist in the system.
    Expects a 401 error and an invalid credentials message.
    """
    resp = client.post("/api/v1/login", json={
        "el_pastas": "nesamas@viko.lt",
        "slaptazodis": "betkas"
    })
    assert resp.status_code == 401
    assert resp.json()["detail"] == "Invalid login credentials"


def test_me_endpoint_success(client, create_test_user):
    """
    Tests the /me endpoint with a valid JWT token.
    Ensures the endpoint returns the correct user profile data.
    """
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
    """
    Tests accessing /me endpoint without an authorization token.
    Expects a 401 or 403 error.
    """
    resp = client.get("/api/v1/me")
    assert resp.status_code == 403 or resp.status_code == 401


def test_change_password_success(client, create_test_user):
    """
    Tests changing the user's password using the /change-password endpoint.
    Verifies that the new password works and (optionally) restores the old password for consistency.
    """
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

    resp = client.post("/api/v1/login", json={
        "el_pastas": TEST_USER["el_pastas"],
        "slaptazodis": new_pw
    })
    assert resp.status_code == 200
    assert "access_token" in resp.json()

    resp = client.post("/api/v1/change-password", json={
        "senas_slaptazodis": new_pw,
        "naujas_slaptazodis": TEST_USER["slaptazodis"]
    }, headers={"Authorization": f"Bearer {resp.json()['access_token']}"})


def test_change_password_wrong_old_pw(client, create_test_user):
    """
    Tests changing the password using an incorrect current password.
    Expects a 400 error and a specific error message.
    """
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
    """
    Tests the /logout endpoint.
    Verifies that it returns a successful logout message and status code 200.
    """
    resp = client.post("/api/v1/logout")
    assert resp.status_code == 200
    assert resp.json()["message"] == "Successfully logged out"