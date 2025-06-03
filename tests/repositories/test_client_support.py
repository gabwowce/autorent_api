"""
Repository tests for Client Support (Klientų palaikymas)

Author: Vytautas Petronis <vytautas.petronis@stud.viko.lt>

Description:
    Unit testai klientų palaikymo repository sluoksniui (CRUD, update, unanswered):
    - get_all, get_by_id, create, update, delete, get_unanswered
    - Edge-case: neegzistuojantis ID, validacija, rollback

Usage:
    pytest tests/repositories/test_client_support.py

Pastabos:
    - Turi būti aprašytas db_session fixture (rollback po kiekvieno testavimo).
    - Importuok schemas/modelius/funcijas tiksliai pagal savo projekto struktūrą!
"""

import pytest
from app.repositories import client_support as support_repo
from app.schemas.client_support import ClientSupportCreate, ClientSupportUpdate

@pytest.fixture
def sample_support_data():
    """Grąžina naujo support užklausos duomenų kopiją (kaip ClientSupportCreate)."""
    return ClientSupportCreate(
        kliento_id=1,              # Testinis klientas turi egzistuoti DB!
        darbuotojo_id=1,           # Testinis darbuotojas turi egzistuoti DB!
        tema="Repo testas",
        pranesimas="Testuojamas palaikymo repo"
    )

def test_create_support(db_session, sample_support_data):
    """
    Testuoja support užklausos sukūrimą per repository.
    """
    support = support_repo.create(db_session, sample_support_data)
    assert support is not None
    assert support.tema == sample_support_data.tema
    assert support.uzklausos_id is not None

def test_get_support_by_id_success(db_session, sample_support_data):
    """
    Testuoja support užklausos gavimą pagal ID (sėkmė).
    """
    support = support_repo.create(db_session, sample_support_data)
    found = support_repo.get_by_id(db_session, support.uzklausos_id)
    assert found is not None
    assert found.uzklausos_id == support.uzklausos_id
    assert found.tema == support.tema

def test_get_support_by_id_not_found(db_session):
    """
    Testuoja gavimą pagal neegzistuojantį ID (turi būti None).
    """
    found = support_repo.get_by_id(db_session, 999999)
    assert found is None

def test_update_support_success(db_session, sample_support_data):
    """
    Testuoja užklausos atnaujinimą (pridėti atsakymą).
    """
    support = support_repo.create(db_session, sample_support_data)
    update_data = ClientSupportUpdate(
        atsakymas="Atsakymas iš testų",
        darbuotojo_id=sample_support_data.darbuotojo_id
    )
    updated = support_repo.update(db_session, support.uzklausos_id, update_data)
    assert updated.atsakymas == "Atsakymas iš testų"
    assert updated.uzklausos_id == support.uzklausos_id

def test_update_support_not_found(db_session):
    """
    Testuoja atnaujinimą neegzistuojančiam support request (turi būti None).
    """
    update_data = ClientSupportUpdate(atsakymas="Testas", darbuotojo_id=1)
    updated = support_repo.update(db_session, 999999, update_data)
    assert updated is None

def test_delete_support_success(db_session, sample_support_data):
    """
    Testuoja support užklausos ištrynimą per repo.
    """
    support = support_repo.create(db_session, sample_support_data)
    result = support_repo.delete(db_session, support.uzklausos_id)
    assert result is True
    found = support_repo.get_by_id(db_session, support.uzklausos_id)
    assert found is None

def test_delete_support_not_found(db_session):
    """
    Testuoja trynimą neegzistuojančiam support request (turi būti False).
    """
    result = support_repo.delete(db_session, 999999)
    assert result is False

def test_get_all_supports(db_session, sample_support_data):
    """
    Testuoja visų support užklausų gavimą (bent 1 turi būti DB po create).
    """
    support = support_repo.create(db_session, sample_support_data)
    supports = support_repo.get_all(db_session)
    assert isinstance(supports, list)
    assert any(s.uzklausos_id == support.uzklausos_id for s in supports)

def test_get_unanswered_supports(db_session, sample_support_data):
    """
    Testuoja neatsakytų užklausų gavimą (atsakymas yra None).
    """
    support = support_repo.create(db_session, sample_support_data)
    unanswered = support_repo.get_unanswered(db_session)
    assert isinstance(unanswered, list)
    assert any(s.uzklausos_id == support.uzklausos_id for s in unanswered)
