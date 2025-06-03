"""
API endpoint tests for Employee management

Author: Vytautas Petronis <vytautas.petronis@stud.viko.lt>

Description:
    Testuoja /api/v1/employees endpointus:
    - Sukūrimas, gavimas pagal ID, visi darbuotojai, atnaujinimas, trynimas
    - Success/failure scenarijai, HATEOAS linkai, validacija

Usage:
    pytest tests/api/test_employee.py
"""

import pytest

EMPLOYEE_SAMPLE = {
    "vardas": "Vardenis",
    "pavarde": "Pavardenis",
    "el_pastas": "employee.test@viko.lt",
    "slaptazodis": "Testas123!",
    "telefono_nr": "+37061111111",
    "pareigos": "Testuotojas",
    "atlyginimas": 1200.50,
    "isidarbinimo_data": "2024-02-01"
}

@pytest.fixture(scope="module")
def created_employee_id(client):
    """Sukuria testinį darbuotoją, po testų jį ištrina."""
    resp = client.post("/api/v1/employees/", json=EMPLOYEE_SAMPLE)
    assert resp.status_code == 200
    emp = resp.json()
    yield emp["darbuotojo_id"]
    client.delete(f"/api/v1/employees/{emp['darbuotojo_id']}")

def test_create_employee(client):
    """Testuoja sėkmingą darbuotojo sukūrimą."""
    data = EMPLOYEE_SAMPLE.copy()
    data["el_pastas"] = "employee.unique@viko.lt"
    resp = client.post("/api/v1/employees/", json=data)
    assert resp.status_code == 200
    emp = resp.json()
    assert emp["el_pastas"] == data["el_pastas"]
    assert "links" in emp
    client.delete(f"/api/v1/employees/{emp['darbuotojo_id']}")

def test_create_employee_missing_required(client):
    """Bando sukurti darbuotoją be el_pastas (tikrina validaciją)."""
    data = EMPLOYEE_SAMPLE.copy()
    data.pop("el_pastas")
    resp = client.post("/api/v1/employees/", json=data)
    assert resp.status_code in (400, 422)

def test_get_all_employees(client, created_employee_id):
    """Gauna visų darbuotojų sąrašą (turi būti bent vienas)."""
    resp = client.get("/api/v1/employees/")
    assert resp.status_code == 200
    employees = resp.json()
    assert isinstance(employees, list)
    assert any(e["darbuotojo_id"] == created_employee_id for e in employees)
    assert all("links" in e for e in employees)

def test_get_employee_by_id(client, created_employee_id):
    """Grąžina darbuotoją pagal ID (sėkmingas atvejis)."""
    resp = client.get(f"/api/v1/employees/{created_employee_id}")
    assert resp.status_code == 200
    emp = resp.json()
    assert emp["darbuotojo_id"] == created_employee_id
    assert "links" in emp
    assert emp["vardas"] == EMPLOYEE_SAMPLE["vardas"]

def test_get_employee_not_found(client):
    """Bando gauti neegzistuojantį darbuotoją pagal ID."""
    resp = client.get("/api/v1/employees/999999")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Employee not found"

def test_update_employee(client, created_employee_id):
    """Testuoja darbuotojo duomenų atnaujinimą (PUT)."""
    update_data = {
        "vardas": "Atnaujintas",
        "pavarde": "Darbuotojas"
    }
    resp = client.put(f"/api/v1/employees/{created_employee_id}", json=update_data)
    assert resp.status_code == 200
    emp = resp.json()
    assert emp["vardas"] == "Atnaujintas"
    assert emp["pavarde"] == "Darbuotojas"
    assert "links" in emp

def test_update_employee_not_found(client):
    """Bando atnaujinti neegzistuojantį darbuotoją."""
    update_data = {"vardas": "Fake"}
    resp = client.put("/api/v1/employees/999999", json=update_data)
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Employee not found"

def test_delete_employee(client):
    """Sukuria ir ištrina darbuotoją."""
    data = EMPLOYEE_SAMPLE.copy()
    data["el_pastas"] = "employee.delete@viko.lt"
    resp = client.post("/api/v1/employees/", json=data)
    assert resp.status_code == 200
    emp_id = resp.json()["darbuotojo_id"]
    resp = client.delete(f"/api/v1/employees/{emp_id}")
    assert resp.status_code == 200
    assert resp.json()["message"] == "Employee deleted successfully"
    resp = client.get(f"/api/v1/employees/{emp_id}")
    assert resp.status_code == 404

def test_delete_employee_not_found(client):
    """Bando ištrinti neegzistuojantį darbuotoją."""
    resp = client.delete("/api/v1/employees/999999")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Employee not found"
