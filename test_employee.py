import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.base import Base
from app.models.employee import Employee
from app.repositories import employee as employee_repo
from datetime import date

# In-memory SQLite DB testavimui
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Sukuriama testinė DB schema
Base.metadata.create_all(bind=engine)

@pytest.fixture()
def db():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture()
def test_employee_data():
    return {
        "vardas": "Jonas",
        "pavarde": "Jonaitis",
        "el_pastas": "jonas@example.com",
        "telefono_nr": "+37060000001",
        "pareigos": "Administratorius",
        "atlyginimas": 1500,
        "isidarbinimo_data": date(2023, 1, 15),
        "slaptazodis": "slaptas123"
    }

def test_create_employee(db, test_employee_data):
    emp = employee_repo.create_employee(db, test_employee_data)
    assert emp.darbuotojo_id is not None
    assert emp.vardas == test_employee_data["vardas"]

def test_get_employee_by_id(db, test_employee_data):
    emp = employee_repo.create_employee(db, test_employee_data)
    result = employee_repo.get_by_id(db, emp.darbuotojo_id)
    assert result is not None
    assert result.el_pastas == test_employee_data["el_pastas"]

def test_get_employee_by_email(db, test_employee_data):
    emp = employee_repo.create_employee(db, test_employee_data)
    result = employee_repo.get_by_email(db, test_employee_data["el_pastas"])
    assert result is not None
    assert result.vardas == test_employee_data["vardas"]

def test_update_employee(db, test_employee_data):
    emp = employee_repo.create_employee(db, test_employee_data)
    update_data = {"pareigos": "Direktorius", "atlyginimas": 2000}
    updated = employee_repo.update(db, emp.darbuotojo_id, update_data)
    assert updated.pareigos == "Direktorius"
    assert updated.atlyginimas == 2000

def test_delete_employee(db, test_employee_data):
    emp = employee_repo.create_employee(db, test_employee_data)
    success = employee_repo.delete(db, emp.darbuotojo_id)
    assert success is True
    assert employee_repo.get_by_id(db, emp.darbuotojo_id) is None
