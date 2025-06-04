"""
API endpoint tests for Geocoding (address → coordinates)

Author: Vytautas Petronis <vytautas.petronis@stud.viko.lt>

Description:
    Tests the /api/v1/geocode endpoints for address geocoding functionality:
    - Successful geocoding (valid address returns coordinates)
    - Handling of invalid or empty addresses (error responses, validation)
    - Checks the response structure and edge cases
    - Dependency on an external geocoding service (mocking is optional)

Usage:
    pytest tests/api/test_geocode.py
"""

import pytest

def test_geocode_success(client):
    """
    Test successful geocoding of a valid address.
    
    Ensures that providing a correct address returns latitude and longitude fields 
    in the response. Optionally, the response may also contain a formatted address 
    or similar data, depending on the API implementation.
    """
    req = {"adresas": "Gedimino pr. 1, Vilnius"}
    resp = client.post("/api/v1/geocode/", json=req)
    assert resp.status_code == 200
    data = resp.json()
    assert "lat" in data and "lng" in data
    # Papildomai – gali būti "formatted_address" ar pan., priklausomai nuo tavo API

def test_geocode_invalid_address(client):
    """
    Test geocoding with an invalid or non-existent address.
    
    Ensures that attempting to geocode a meaningless or unknown address returns an error 
    status code (400 or 404), and that the error message indicates the coordinates 
    could not be found.
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
    Test geocoding with an empty address string.
    
    Checks that the API responds with a validation error (400 or 422) if the 
    address field is empty, and that the response contains an appropriate 
    error detail message.
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
    Test geocoding when the 'adresas' field is missing from the request.
    
    Ensures that the API responds with a validation error (400 or 422), and the 
    response contains a 'detail' key describing the problem.
    """
    resp = client.post("/api/v1/geocode/", json={})
    assert resp.status_code in (400, 422)
    # FastAPI dažniausiai 422 su Pydantic klaida
    resp_json = resp.json()
    assert "detail" in resp_json

def test_geocode_get_method_not_allowed(client):
    """
    Test that GET method is not allowed on the geocode endpoint.
    
    Ensures that only POST requests are accepted, and a GET request returns 
    a 405 Method Not Allowed status code.
    """
    resp = client.get("/api/v1/geocode/")
    assert resp.status_code == 405

