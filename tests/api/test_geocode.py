"""
API endpoint tests for Geocoding (adresų → koordinatės)

Author: Vytautas Petronis <vytautas.petronis@stud.viko.lt>

Description:
    Testuoja /api/v1/geocode endpointus:
    - Sėkmingas ir nesėkmingas (klaidingas/tuščias adresas) geokodavimas
    - Response struktūra, validacija, edge-case
    - Priklausomybė nuo išorinio serviso (mock'inti nebūtina, bet galima!)

Usage:
    pytest tests/api/test_geocode.py
"""

import pytest

def test_geocode_success(client):
    """
    Testuoja sėkmingą geokodavimą (teisingas adresas).
    """
    req = {"adresas": "Gedimino pr. 1, Vilnius"}
    resp = client.post("/api/v1/geocode/", json=req)
    assert resp.status_code == 200
    data = resp.json()
    assert "lat" in data and "lng" in data
    # Papildomai – gali būti "formatted_address" ar pan., priklausomai nuo tavo API

def test_geocode_invalid_address(client):
    """
    Testuoja nesėkmingą geokodavimą (neegzistuojantis ar beprasmis adresas).
    """
    req = {"adresas": "QWERTYUIOP1234567890, Marsas"}
    resp = client.post("/api/v1/geocode/", json=req)
    # Priklausomai nuo API – gali būti 404, 400 arba speciali error žinutė
    assert resp.status_code in (400, 404)
    detail = resp.json().get("detail", "")
    assert (
        "not found" in detail.lower()
        or "nepavyko" in detail.lower()
        or "koordinatės nerastos" in detail.lower()
    )

def test_geocode_empty_address(client):
    """
    Testuoja geokodavimą be adreso (tikrina validaciją).
    """
    req = {"adresas": ""}
    resp = client.post("/api/v1/geocode/", json=req)
    assert resp.status_code in (400, 422)
    # Gali būti Pydantic klaida, arba custom "adresas turi būti nurodytas"
    # Patikrina error žinutę
    detail = resp.json().get("detail", "")
    assert detail or isinstance(resp.json(), dict)

def test_geocode_missing_field(client):
    """
    Testuoja, kai visai nėra 'adresas' lauko request'e.
    """
    resp = client.post("/api/v1/geocode/", json={})
    assert resp.status_code in (400, 422)
    # FastAPI dažniausiai 422 su Pydantic klaida
    resp_json = resp.json()
    assert "detail" in resp_json

def test_geocode_get_method_not_allowed(client):
    """
    Tik POST metodas leidžiamas, GET turi mesti 405.
    """
    resp = client.get("/api/v1/geocode/")
    assert resp.status_code == 405

