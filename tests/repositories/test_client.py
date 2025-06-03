"""
Repository tests for Client (Klientai)

Author: Vytautas Petronis <vytautas.petronis@stud.viko.lt>

Description:
    Unit testai klientų repository sluoksniui (CRUD metodai):
    - get_all, get_by_id, create, delete
    - Edge-case: neegzistuojantis ID, validacijos, rollback (testinė DB)

Usage:
    pytest tests/repositories/test_client.py

Pastabos:
    - Turi būti `db_session` fixture (pvz., per conftest.py, kuri rollback'ina DB).
    - Importuok schemas/modelius/funcijas tiksliai pagal savo projekto struktūrą!
"""

import pytest
from app.repositories import client as client_repo
from app.schemas.client import ClientCreate

@pytest.fixture
def sample_client_data():
    """Grąžina naujo kliento duomenų kopiją (kaip ClientCreate)."""
    return ClientCreate(
        vardas="Testas",
        pavarde="Repo",
        el_pastas="repo.test@viko.lt",
        telefono_nr="+37069999999",
        gimimo_data="1990-01-01"
    )

def test_create_client(db_session, sample_client_data):
    """
    Testuoja kliento sukūrimą per repository.
    """
    new_client = client_repo.create(db_session, sample_client_data)
    assert new_client is not None
    assert new_client.el_pastas == sample_client_data.el_pastas
    assert new_client.kliento_id is not None

def test_get_client_by_id_success(db_session, sample_client_data):
    """
    Testuoja kliento gavimą pagal ID (sėkmingas atvejis).
    """
    client = client_repo.create(db_session, sample_client_data)
    found = client_repo.get_by_id(db_session, client.kliento_id)
    assert found is not None
    assert found.kliento_id == client.kliento_id
    assert found.vardas == client.vardas

def test_get_client_by_id_not_found(db_session):
    """
    Testuoja gavimą pagal neegzistuojantį ID (turi būti None).
    """
    found = client_repo.get_by_id(db_session, 999999)
    assert found is None

def test_delete_client_success(db_session, sample_client_data):
    """
    Testuoja kliento ištrynimą (delete per repo).
    """
    client = client_repo.create(db_session, sample_client_data)
    result = client_repo.delete(db_session, client.kliento_id)
    assert result is True
    # Įsitikina, kad kliento nebėra
    found = client_repo.get_by_id(db_session, client.kliento_id)
    assert found is None

def test_delete_client_not_found(db_session):
    """
    Testuoja trynimą neegzistuojančiam klientui (turi būti False).
    """
    result = client_repo.delete(db_session, 999999)
    assert result is False

def test_get_all_clients(db_session, sample_client_data):
    """
    Testuoja visų klientų gavimą (bent 1 turi būti DB po create).
    """
    client = client_repo.create(db_session, sample_client_data)
    clients = client_repo.get_all(db_session)
    assert isinstance(clients, list)
    assert any(c.kliento_id == client.kliento_id for c in clients)
