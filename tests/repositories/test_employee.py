"""
Repository tests for Employee (Darbuotojai)

Author: Vytautas Petronis <vytautas.petronis@stud.viko.lt>

Description:
    Unit testai darbuotojų repository sluoksniui (CRUD metodai):
    - get_all, get_by_id, create, update, delete
    - Edge-case: neegzistuojantis ID, rollback (testinė DB)

Usage:
    pytest tests/repositories/test_employee.py

Pastabos:
    - Reikalingas db_session fixture (conftest.py)
    - Importuok schemas/modelius/funcijas pagal savo projekto struktūrą!
"""

import pytest
from app.repositories import employee as employee_repo
from app.schemas.employee import EmployeeCreate, EmployeeUpdate

@pytest.fixture
def sample_employee_data():
    """Grąžina naujo darbuotojo duomenų kopiją (kaip EmployeeCreate)."""
    return EmployeeCreate(
        vardas="Astijus",
        pavarde="UnitTest",
        el_pastas="employee.repo@viko.lt",
        slaptazodis="Testas123!",
        telefono_nr="+37067778888",
        pareigos="Testuotojas",
        atlyginimas=1200.0,
        isidarbinimo_data="2024-04-01"
    )

def test_create_employee(db_session, sample_employee_data):
    """
    Testuoja darbuotojo sukūrimą per repository.
    """
    employee = employee_repo.create(db_session, sample_employee_data)
    assert employee is not None
    assert employee.el_pastas == sample_employee_data.el_pastas
    assert employee.darbuotojo_id is not None

def test_get_employee_by_id_success(db_session, sample_employee_data):
    """
    Testuoja darbuotojo gavimą pagal ID (sėkmė).
    """
    employee = employee_repo.create(db_session, sample_employee_data)
    found = employee_repo.get_by_id(db_session, employee.darbuotojo_id)
    assert found is not None
    assert found.darbuotojo_id == employee.darbuotojo_id
    assert found.vardas == employee.vardas

def test_get_employee_by_id_not_found(db_session):
    """
    Testuoja gavimą pagal neegzistuojantį ID (turi būti None).
    """
    found = employee_repo.get_by_id(db_session, 999999)
    assert found is None

def test_update_employee_success(db_session, sample_employee_data):
    """
    Testuoja darbuotojo atnaujinimą (update per repo).
    """
    employee = employee_repo.create(db_session, sample_employee_data)
    update_data = EmployeeUpdate(
        vardas="Atnaujintas",
        pavarde="Darbuotojas",
        el_pastas=employee.el_pastas,
        slaptazodis=employee.slaptazodis,
        telefono_nr=employee.telefono_nr,
        pareigos="Vadybininkas",
        atlyginimas=1300.0,
        isidarbinimo_data=employee.isidarbinimo_data
    )
    updated = employee_repo.update(db_session, employee.darbuotojo_id, update_data)
    assert updated.vardas == "Atnaujintas"
    assert updated.pavarde == "Darbuotojas"
    assert updated.pareigos == "Vadybininkas"
    assert updated.darbuotojo_id == employee.darbuotojo_id

def test_update_employee_not_found(db_session):
    """
    Testuoja atnaujinimą neegzistuojančiam darbuotojui (turi būti None).
    """
    update_data = EmployeeUpdate(
        vardas="Fake",
        pavarde="Darbuotojas",
        el_pastas="fake@viko.lt",
        slaptazodis="slaptas",
        telefono_nr="+37067779999",
        pareigos="Nėra",
        atlyginimas=0.0,
        isidarbinimo_data="2024-01-01"
    )
    updated = employee_repo.update(db_session, 999999, update_data)
    assert updated is None

def test_delete_employee_success(db_session, sample_employee_data):
    """
    Testuoja darbuotojo ištrynimą per repo.
    """
    employee = employee_repo.create(db_session, sample_employee_data)
    result = employee_repo.delete(db_session, employee.darbuotojo_id)
    assert result is True
    found = employee_repo.get_by_id(db_session, employee.darbuotojo_id)
    assert found is None

def test_delete_employee_not_found(db_session):
    """
    Testuoja trynimą neegzistuojančiam darbuotojui (turi būti False).
    """
    result = employee_repo.delete(db_session, 999999)
    assert result is False

def test_get_all_employees(db_session, sample_employee_data):
    """
    Testuoja visų darbuotojų gavimą (bent 1 turi būti DB po create).
    """
    employee = employee_repo.create(db_session, sample_employee_data)
    employees = employee_repo.get_all(db_session)
    assert isinstance(employees, list)
    assert any(e.darbuotojo_id == employee.darbuotojo_id for e in employees)
