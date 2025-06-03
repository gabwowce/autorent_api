"""
Repository tests for Invoice (Sąskaitos)

Author: Vytautas Petronis <vytautas.petronis@stud.viko.lt>

Description:
    Unit testai sąskaitų repository sluoksniui (CRUD metodai):
    - get_all, get_by_id, create, update, delete
    - Edge-case: neegzistuojantis ID, rollback (testinė DB)

Usage:
    pytest tests/repositories/test_invoice.py

Pastabos:
    - Reikalingas db_session fixture (conftest.py)
    - Importuok schemas/modelius/funcijas pagal savo projekto struktūrą!
"""

import pytest
from app.repositories import invoice as invoice_repo
from app.schemas.invoice import InvoiceCreate, InvoiceUpdate

@pytest.fixture
def sample_invoice_data():
    """Grąžina naujos sąskaitos duomenų kopiją (kaip InvoiceCreate)."""
    return InvoiceCreate(
        uzsakymo_id=1,          # Užsakymas turi egzistuoti testinėje DB!
        suma=150.0,
        israsymo_data="2024-06-01",
        busena="apmokėta"
    )

def test_create_invoice(db_session, sample_invoice_data):
    """
    Testuoja sąskaitos sukūrimą per repository.
    """
    invoice = invoice_repo.create(db_session, sample_invoice_data)
    assert invoice is not None
    assert invoice.suma == sample_invoice_data.suma
    assert invoice.saskaitos_id is not None

def test_get_invoice_by_id_success(db_session, sample_invoice_data):
    """
    Testuoja sąskaitos gavimą pagal ID (sėkmingas atvejis).
    """
    invoice = invoice_repo.create(db_session, sample_invoice_data)
    found = invoice_repo.get_by_id(db_session, invoice.saskaitos_id)
    assert found is not None
    assert found.saskaitos_id == invoice.saskaitos_id
    assert found.uzsakymo_id == invoice.uzsakymo_id

def test_get_invoice_by_id_not_found(db_session):
    """
    Testuoja gavimą pagal neegzistuojantį ID (turi būti None).
    """
    found = invoice_repo.get_by_id(db_session, 999999)
    assert found is None

def test_update_invoice_success(db_session, sample_invoice_data):
    """
    Testuoja sąskaitos atnaujinimą (update per repo).
    """
    invoice = invoice_repo.create(db_session, sample_invoice_data)
    update_data = InvoiceUpdate(
        suma=99.99,
        busena="neapmokėta"
    )
    updated = invoice_repo.update(db_session, invoice.saskaitos_id, update_data)
    assert updated.suma == 99.99
    assert updated.busena == "neapmokėta"
    assert updated.saskaitos_id == invoice.saskaitos_id

def test_update_invoice_not_found(db_session):
    """
    Testuoja atnaujinimą neegzistuojančiai sąskaitai (turi būti None).
    """
    update_data = InvoiceUpdate(suma=10.0, busena="apmokėta")
    updated = invoice_repo.update(db_session, 999999, update_data)
    assert updated is None

def test_delete_invoice_success(db_session, sample_invoice_data):
    """
    Testuoja sąskaitos ištrynimą per repo.
    """
    invoice = invoice_repo.create(db_session, sample_invoice_data)
    result = invoice_repo.delete(db_session, invoice.saskaitos_id)
    assert result is True
    found = invoice_repo.get_by_id(db_session, invoice.saskaitos_id)
    assert found is None

def test_delete_invoice_not_found(db_session):
    """
    Testuoja trynimą neegzistuojančiai sąskaitai (turi būti False).
    """
    result = invoice_repo.delete(db_session, 999999)
    assert result is False

def test_get_all_invoices(db_session, sample_invoice_data):
    """
    Testuoja visų sąskaitų gavimą (bent 1 turi būti DB po create).
    """
    invoice = invoice_repo.create(db_session, sample_invoice_data)
    invoices = invoice_repo.get_all(db_session)
    assert isinstance(invoices, list)
    assert any(inv.saskaitos_id == invoice.saskaitos_id for inv in invoices)
