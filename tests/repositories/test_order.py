"""
Repository tests for Order (Užsakymai)

Author: Vytautas Petronis <vytautas.petronis@stud.viko.lt>

Description:
    Unit testai užsakymų repository sluoksniui (CRUD metodai):
    - get_all, get_by_id, create, update, delete
    - Edge-case: neegzistuojantis ID, rollback (testinė DB)

Usage:
    pytest tests/repositories/test_order.py

Pastabos:
    - Reikalingas db_session fixture (conftest.py)
    - Importuok schemas/modelius/funcijas pagal savo projekto struktūrą!
"""

import pytest
from app.repositories import order as order_repo
from app.schemas.order import OrderCreate, OrderUpdate

@pytest.fixture
def sample_order_data():
    """Grąžina naujo užsakymo duomenų kopiją (kaip OrderCreate)."""
    return OrderCreate(
        kliento_id=1,           # Testinis klientas turi egzistuoti DB!
        automobilio_id=1,       # Testinis automobilis turi egzistuoti DB!
        nuomos_pradzia="2024-07-01",
        nuomos_pabaiga="2024-07-10",
        busena="patvirtintas",
        kaina=300.0,
        pasto_adresas="Kauno g. 1, Vilnius"
    )

def test_create_order(db_session, sample_order_data):
    """
    Testuoja užsakymo sukūrimą per repository.
    """
    order = order_repo.create(db_session, sample_order_data)
    assert order is not None
    assert order.kaina == sample_order_data.kaina
    assert order.uzsakymo_id is not None

def test_get_order_by_id_success(db_session, sample_order_data):
    """
    Testuoja užsakymo gavimą pagal ID (sėkmė).
    """
    order = order_repo.create(db_session, sample_order_data)
    found = order_repo.get_by_id(db_session, order.uzsakymo_id)
    assert found is not None
    assert found.uzsakymo_id == order.uzsakymo_id
    assert found.kliento_id == order.kliento_id

def test_get_order_by_id_not_found(db_session):
    """
    Testuoja gavimą pagal neegzistuojantį ID (turi būti None).
    """
    found = order_repo.get_by_id(db_session, 999999)
    assert found is None

def test_update_order_success(db_session, sample_order_data):
    """
    Testuoja užsakymo atnaujinimą (update per repo).
    """
    order = order_repo.create(db_session, sample_order_data)
    update_data = OrderUpdate(
        nuomos_pradzia=order.nuomos_pradzia,
        nuomos_pabaiga=order.nuomos_pabaiga,
        busena="atšauktas",
        kaina=0.0,
        pasto_adresas=order.pasto_adresas
    )
    updated = order_repo.update(db_session, order.uzsakymo_id, update_data)
    assert updated.busena == "atšauktas"
    assert updated.kaina == 0.0
    assert updated.uzsakymo_id == order.uzsakymo_id

def test_update_order_not_found(db_session):
    """
    Testuoja atnaujinimą neegzistuojančiam užsakymui (turi būti None).
    """
    update_data = OrderUpdate(
        nuomos_pradzia="2024-08-01",
        nuomos_pabaiga="2024-08-10",
        busena="atšauktas",
        kaina=0.0,
        pasto_adresas="Fake"
    )
    updated = order_repo.update(db_session, 999999, update_data)
    assert updated is None

def test_delete_order_success(db_session, sample_order_data):
    """
    Testuoja užsakymo ištrynimą per repo.
    """
    order = order_repo.create(db_session, sample_order_data)
    result = order_repo.delete(db_session, order.uzsakymo_id)
    assert result is True
    found = order_repo.get_by_id(db_session, order.uzsakymo_id)
    assert found is None

def test_delete_order_not_found(db_session):
    """
    Testuoja trynimą neegzistuojančiam užsakymui (turi būti False).
    """
    result = order_repo.delete(db_session, 999999)
    assert result is False

def test_get_all_orders(db_session, sample_order_data):
    """
    Testuoja visų užsakymų gavimą (bent 1 turi būti DB po create).
    """
    order = order_repo.create(db_session, sample_order_data)
    orders = order_repo.get_all(db_session)
    assert isinstance(orders, list)
    assert any(o.uzsakymo_id == order.uzsakymo_id for o in orders)
