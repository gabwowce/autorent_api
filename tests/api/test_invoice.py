"""
Automated tests for Invoice API endpoints.

Author: Vytautas Petronis <vytautas.petronis@stud.viko.lt>

Description:
    Integration tests for the /invoices endpoints of the Car Rental RESTful API.
    Tests include creating, retrieving, updating status, and deleting invoices.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from uuid import uuid4

client = TestClient(app)

@pytest.fixture
def prepared_order():
    """
    Prepares an order for tests by creating necessary related data:
    location, car, employee, and client via API POST requests.

    Steps:
    1. Create a location and get its ID.
    2. Create a car assigned to that location.
    3. Create an employee.
    4. Create a client.
    5. Create an order linking client, car, and employee.
    6. Return the order ID for use in tests.

    Asserts that all created entities have their IDs.
    """
    location_resp = client.post("/api/v1/locations/", json={
        "pavadinimas": "Vilnius Centras",
        "adresas": "Gedimino pr. 1",
        "miestas": "Vilnius"
    })
    location_id = 1
    if location_resp.status_code in [200, 201]:
        location_id = location_resp.json().get("vietos_id", 1)
    
    car_resp = client.post("/api/v1/cars/", json={
        "marke": "Toyota",
        "modelis": "Corolla",
        "metai": 2021,
        "numeris": f"ABC{uuid4().hex[:3].upper()}",
        "vin_kodas": uuid4().hex[:16].upper(),
        "spalva": "Juoda",
        "kebulo_tipas": "Sedanas",
        "pavarų_deze": "Automatinė",
        "variklio_turis": 1.6,
        "galia_kw": 97,
        "kuro_tipas": "Benzinas",
        "rida": 15000,
        "sedimos_vietos": 5,
        "klimato_kontrole": True,
        "navigacija": True,
        "kaina_parai": 40.00,
        "automobilio_statusas": "laisvas",
        "technikines_galiojimas": "2025-12-31",
        "dabartine_vieta_id": location_id,
        "pastabos": "Testinis auto"
    })
    car_id = car_resp.json().get("automobilio_id") or car_resp.json().get("id")
    assert car_id is not None, f"Nėra automobilio_id! car_resp: {car_resp.json()}"

    emp_resp = client.post("/api/v1/employees/", json={
        "vardas": "Testas",
        "pavarde": "Darbuotojas",
        "el_pastas": f"darbuotojas{uuid4().hex[:6]}@viko.lt",
        "slaptazodis": "slaptas123!",
        "telefono_nr": "+37060000002",
        "pareigos": "Administratorius",
        "atlyginimas": 1800.00,
        "isidarbinimo_data": "2023-01-01"
    })
    emp_id = emp_resp.json().get("darbuotojo_id") or emp_resp.json().get("id")
    assert emp_id is not None, f"Nėra darbuotojo_id! emp_resp: {emp_resp.json()}"

    el_pastas = f"testas{uuid4().hex[:8]}@viko.lt"
    client_resp = client.post("/api/v1/clients/", json={
        "vardas": "Testas",
        "pavarde": "Testavičius",
        "el_pastas": el_pastas,
        "telefono_nr": "+37060000000",
        "slaptazodis": "labaiSaugus123!",
        "gimimo_data": "2000-01-01",
        "registracijos_data": "2024-06-01",
        "bonus_taskai": 0
    })
    resp_json = client_resp.json()
    client_id = (
        resp_json.get("kliento_id")
        or resp_json.get("client_id")
        or resp_json.get("id")
        or (resp_json.get("data", {}).get("kliento_id") if resp_json.get("data") else None)
    )
    assert client_id is not None, f"Nėra kliento_id! client_resp: {client_resp.json()}"

    order_body = {
        "kliento_id": client_id,
        "automobilio_id": car_id,
        "darbuotojo_id": emp_id,
        "nuomos_data": "2024-06-01",
        "grazinimo_data": "2024-06-10",
        "paemimo_vietos_id": 1,          
        "grazinimo_vietos_id": 1,         
        "bendra_kaina": 100.0,
        "uzsakymo_busena": "patvirtinta",
        "turi_papildomas_paslaugas": False
    }
    order_resp = client.post("/api/v1/orders/", json=order_body)
    order_id = order_resp.json().get("uzsakymo_id") or order_resp.json().get("order_id")
    assert order_id is not None, f"Nėra order_id! order_resp: {order_resp.json()}"
    return order_id

@pytest.fixture
def example_invoice_data(prepared_order):
    """
    Provides example data for creating a new invoice.
    Uses the order ID from the prepared_order fixture.
    """
    return {
        "order_id": prepared_order,
        "total": 123.45,
        "invoice_date": "2024-06-01"
    }

def assert_invoiceout_fields(data):
    """
    Validates that the InvoiceOut response contains all required fields
    and that each field has the expected type.

    Expected fields and types:
        - invoice_id: int
        - order_id: int
        - kliento_id: int
        - total: float or int
        - invoice_date: str (ISO formatted date)
        - status: str
        - client_first_name: str
        - client_last_name: str
        - links: list
    """
    expected_fields = [
        "invoice_id", "order_id", "kliento_id", "total", "invoice_date",
        "status", "client_first_name", "client_last_name", "links"
    ]
    for field in expected_fields:
        assert field in data, f"Trūksta lauko: {field}"

    assert isinstance(data["invoice_id"], int)
    assert isinstance(data["order_id"], int)
    assert isinstance(data["kliento_id"], int)
    assert isinstance(data["total"], float) or isinstance(data["total"], int)
    assert isinstance(data["invoice_date"], str)  # grįžta kaip ISO formatas
    assert isinstance(data["status"], str)
    assert isinstance(data["client_first_name"], str)
    assert isinstance(data["client_last_name"], str)
    assert isinstance(data["links"], list)

def test_create_invoice(example_invoice_data):
    """
    Tests creating a new invoice via POST /invoices/ endpoint.
    Verifies successful response status and correctness of returned fields.
    """
    response = client.post("/api/v1/invoices/", json=example_invoice_data)
    assert response.status_code in [200, 201]
    data = response.json()
    assert_invoiceout_fields(data)
    assert data["order_id"] == example_invoice_data["order_id"]
    assert float(data["total"]) == example_invoice_data["total"]
    assert data["invoice_date"] == example_invoice_data["invoice_date"]

def test_get_all_invoices():
    """
    Tests retrieving all invoices via GET /invoices/ endpoint.
    Verifies response status and that the returned data is a list.
    If there are invoices, validates the first one’s fields.
    """
    response = client.get("/api/v1/invoices/")
    assert response.status_code == 200
    invoices = response.json()
    assert isinstance(invoices, list)
    if invoices:
        assert_invoiceout_fields(invoices[0])

def test_update_invoice_status(prepared_order):
    """
    Tests updating an invoice’s status via PATCH /invoices/{invoice_id}/status.
    Creates a new invoice, updates its status, and checks the response.
    """
    invoice_resp = client.post("/api/v1/invoices/", json={
        "order_id": prepared_order,
        "total": 50.0,
        "invoice_date": "2024-06-01"
    })
    assert invoice_resp.status_code in [200, 201]
    invoice_id = invoice_resp.json()["invoice_id"]

    update_resp = client.patch(f"/api/v1/invoices/{invoice_id}/status", json={"status": "apmokėta"})
    assert update_resp.status_code == 200
    data = update_resp.json()
    assert_invoiceout_fields(data)
    assert data["status"] in ["apmokėta", "patvirtinta"]


def test_delete_invoice(prepared_order):
    """
    Tests deleting an invoice via DELETE /invoices/{invoice_id} endpoint.
    Creates an invoice, deletes it, and verifies successful deletion.
    Confirms the invoice is no longer present when listing all invoices.
    """
    invoice_resp = client.post("/api/v1/invoices/", json={
        "order_id": prepared_order,
        "total": 77.7,
        "invoice_date": "2024-06-01"
    })
    invoice_id = invoice_resp.json()["invoice_id"]

    del_resp = client.delete(f"/api/v1/invoices/{invoice_id}")
    assert del_resp.status_code in [200, 204]
    if del_resp.status_code == 200:
        assert del_resp.json()["detail"] == "Invoice deleted"

    get_resp = client.get("/api/v1/invoices/")
    ids = [inv["invoice_id"] for inv in get_resp.json()]
    assert invoice_id not in ids
