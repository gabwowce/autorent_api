"""
Repository tests for Reservation (Rezervacijos)

Author: Vytautas Petronis <vytautas.petronis@stud.viko.lt>

Description:
    Unit testai rezervacijų repository sluoksniui (CRUD metodai):
    - get_all, get_by_id, create, update, delete
    - Edge-case: neegzistuojantis ID, rollback (testinė DB)

Usage:
    pytest tests/repositories/test_reservation.py

Pastabos:
    - Reikalingas db_session fixture (conftest.py)
    - Importuok schemas/modelius/funcijas pagal savo projekto struktūrą!
"""

import pytest
from app.repositories import rest_reservation as reservation_repo
from app.schemas.reservation import ReservationCreate, ReservationUpdate

@pytest.fixture
def sample_reservation_data():
    """Grąžina naujos rezervacijos duomenų kopiją (kaip ReservationCreate)."""
    return ReservationCreate(
        kliento_id=1,           # Testinis klientas turi egzistuoti DB!
        automobilio_id=1,       # Testinis automobilis turi egzistuoti DB!
        rezervacijos_pradzia="2024-07-01",
        rezervacijos_pabaiga="2024-07-05",
        pasto_adresas="A. Goštauto g. 12, Vilnius"
    )

def test_create_reservation(db_session, sample_reservation_data):
    """
    Testuoja rezervacijos sukūrimą per repository.
    """
    reservation = reservation_repo.create(db_session, sample_reservation_data)
    assert reservation is not None
    assert reservation.kliento_id == sample_reservation_data.kliento_id
    assert reservation.rezervacijos_id is not None

def test_get_reservation_by_id_success(db_session, sample_reservation_data):
    """
    Testuoja rezervacijos gavimą pagal ID (sėkmingas atvejis).
    """
    reservation = reservation_repo.create(db_session, sample_reservation_data)
    found = reservation_repo.get_by_id(db_session, reservation.rezervacijos_id)
    assert found is not None
    assert found.rezervacijos_id == reservation.rezervacijos_id
    assert found.automobilio_id == reservation.automobilio_id

def test_get_reservation_by_id_not_found(db_session):
    """
    Testuoja gavimą pagal neegzistuojantį ID (turi būti None).
    """
    found = reservation_repo.get_by_id(db_session, 999999)
    assert found is None

def test_update_reservation_success(db_session, sample_reservation_data):
    """
    Testuoja rezervacijos atnaujinimą (update per repo).
    """
    reservation = reservation_repo.create(db_session, sample_reservation_data)
    update_data = ReservationUpdate(
        rezervacijos_pradzia=reservation.rezervacijos_pradzia,
        rezervacijos_pabaiga="2024-07-10",
        pasto_adresas="Naujas adresas"
    )
    updated = reservation_repo.update(db_session, reservation.rezervacijos_id, update_data)
    assert updated.rezervacijos_id == reservation.rezervacijos_id
    assert updated.rezervacijos_pabaiga == "2024-07-10"
    assert updated.pasto_adresas == "Naujas adresas"

def test_update_reservation_not_found(db_session):
    """
    Testuoja atnaujinimą neegzistuojančiai rezervacijai (turi būti None).
    """
    update_data = ReservationUpdate(
        rezervacijos_pradzia="2024-08-01",
        rezervacijos_pabaiga="2024-08-03",
        pasto_adresas="Fake"
    )
    updated = reservation_repo.update(db_session, 999999, update_data)
    assert updated is None

def test_delete_reservation_success(db_session, sample_reservation_data):
    """
    Testuoja rezervacijos ištrynimą per repo.
    """
    reservation = reservation_repo.create(db_session, sample_reservation_data)
    result = reservation_repo.delete(db_session, reservation.rezervacijos_id)
    assert result is True
    found = reservation_repo.get_by_id(db_session, reservation.rezervacijos_id)
    assert found is None

def test_delete_reservation_not_found(db_session):
    """
    Testuoja trynimą neegzistuojančiai rezervacijai (turi būti False).
    """
    result = reservation_repo.delete(db_session, 999999)
    assert result is False

def test_get_all_reservations(db_session, sample_reservation_data):
    """
    Testuoja visų rezervacijų gavimą (bent 1 turi būti DB po create).
    """
    reservation = reservation_repo.create(db_session, sample_reservation_data)
    reservations = reservation_repo.get_all(db_session)
    assert isinstance(reservations, list)
    assert any(r.rezervacijos_id == reservation.rezervacijos_id for r in reservations)
