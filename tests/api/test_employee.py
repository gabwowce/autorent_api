"""
API endpoint tests for Employee management

Author: Vytautas Petronis <vytautas.petronis@stud.viko.lt>

Description:
    Automated tests for the /api/v1/employees endpoints of the Car Rental API.
    This test suite covers all CRUD operations for employees, including:
    - Creation, retrieval by ID, listing all, updating, and deletion of employees
    - Both successful and failure scenarios (such as validation errors or not found)
    - Validation of response structure, including HATEOAS links

Usage:
    pytest tests/api/test_employee.py

Notes:
    - Import all necessary dependencies and fixtures according to your project structure.
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
    """
    Fixture: Creates a sample employee at the start of the test module and deletes it at the end.
    Returns the ID of the created employee to be used in other tests.
    """
    resp = client.post("/api/v1/employees/", json=EMPLOYEE_SAMPLE)
    assert resp.status_code == 200
    emp = resp.json()
    yield emp["darbuotojo_id"]
    client.delete(f"/api/v1/employees/{emp['darbuotojo_id']}")

def test_create_employee(client):
    """
    Test: Successful creation of a new employee.
    Verifies that the employee is created, data is returned, and HATEOAS links are present.
    """
    data = EMPLOYEE_SAMPLE.copy()
    data["el_pastas"] = "employee.unique@viko.lt"
    resp = client.post("/api/v1/employees/", json=data)
    assert resp.status_code == 200
    emp = resp.json()
    assert emp["el_pastas"] == data["el_pastas"]
    assert "links" in emp
    client.delete(f"/api/v1/employees/{emp['darbuotojo_id']}")

def test_create_employee_missing_required(client):
    """
    Test: Attempt to create an employee without a required field ('el_pastas').
    Expects a validation error response.
    """
    data = EMPLOYEE_SAMPLE.copy()
    data.pop("el_pastas")
    resp = client.post("/api/v1/employees/", json=data)
    assert resp.status_code in (400, 422)

def test_get_all_employees(client, created_employee_id):
    """
    Test: Retrieve the list of all employees.
    Checks that the created employee is present in the list and that all responses contain HATEOAS links.
    """
    resp = client.get("/api/v1/employees/")
    assert resp.status_code == 200
    employees = resp.json()
    assert isinstance(employees, list)
    assert any(e["darbuotojo_id"] == created_employee_id for e in employees)
    assert all("links" in e for e in employees)

def test_get_employee_by_id(client, created_employee_id):
    """
    Test: Retrieve a single employee by ID (successful case).
    Verifies returned data, structure, and HATEOAS links.
    """
    resp = client.get(f"/api/v1/employees/{created_employee_id}")
    assert resp.status_code == 200
    emp = resp.json()
    assert emp["darbuotojo_id"] == created_employee_id
    assert "links" in emp
    assert emp["vardas"] == EMPLOYEE_SAMPLE["vardas"]

def test_get_employee_not_found(client):
    """
    Test: Attempt to retrieve a non-existent employee by ID.
    Expects a 404 Not Found error and a descriptive error message.
    """
    resp = client.get("/api/v1/employees/999999")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Employee not found"

def test_update_employee(client, created_employee_id):
    """
    Test: Update an employee's information using PUT.
    Verifies that changes are applied and response contains HATEOAS links.
    """
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
    """
    Test: Attempt to update a non-existent employee.
    Expects a 404 Not Found error and a descriptive error message.
    """
    update_data = {"vardas": "Fake"}
    resp = client.put("/api/v1/employees/999999", json=update_data)
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Employee not found"

def test_delete_employee(client):
    """
    Test: Create and then delete an employee.
    Verifies successful deletion and ensures the employee is no longer retrievable.
    """
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
    """
    Test: Attempt to delete a non-existent employee.
    Expects a 404 Not Found error and a descriptive error message.
    """
    resp = client.delete("/api/v1/employees/999999")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Employee not found"
