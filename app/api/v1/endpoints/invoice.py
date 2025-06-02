"""
app/api/v1/endpoints/invoice.py

API endpoints for invoice management.

Author: Vytautas Petronis <vytautas.petronis@stud.viko.lt>

Description:
    Implements RESTful API routes for invoice CRUD operations and status updates.
    All endpoints return data with HATEOAS links for easier frontend navigation.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas.invoice import InvoiceCreate, InvoiceStatusUpdate, InvoiceOut
from app.repositories import invoice as crud_invoice
from utils.hateoas import generate_links

router = APIRouter(
    prefix="/invoices",
    tags=["Invoices"]
)

def generate_invoice_links(invoice) -> list[dict]:
    """
    Build HATEOAS links for an invoice.

    Args:
        invoice (Invoice or dict): Invoice instance or dict.

    Returns:
        list[dict]: List of navigation links.

    Author: Vytautas Petronis <vytautas.petronis@stud.viko.lt>
    """
    get = lambda obj, key: obj.get(key) if isinstance(obj, dict) else getattr(obj, key)
    return [
        {"rel": "self", "href": f"/invoices/{get(invoice, 'saskaitos_id')}"},
        {"rel": "order", "href": f"/orders/{get(invoice, 'uzsakymo_id')}"},
        {"rel": "update_status", "href": f"/invoices/{get(invoice, 'saskaitos_id')}/status"},
        {"rel": "delete", "href": f"/invoices/{get(invoice, 'saskaitos_id')}"}
    ]


@router.get("/", response_model=list[InvoiceOut], operation_id="getAllInvoices")
def get_all_invoices(db: Session = Depends(get_db)):
    """
    Retrieve all invoices.

    Args:
        db (Session): SQLAlchemy session.

    Returns:
        list[InvoiceOut]: List of invoices with HATEOAS links.

    Author: Vytautas Petronis <vytautas.petronis@stud.viko.lt>
    """
    raw_data = crud_invoice.get_invoice(db)
    return [
        {
            **invoice,
            "links": generate_invoice_links(invoice)
        }
        for invoice in raw_data
    ]

@router.post("/", response_model=InvoiceOut, operation_id="createInvoice")
def create_invoice(invoice: InvoiceCreate, db: Session = Depends(get_db)):
    """
    Create a new invoice.

    Args:
        invoice (InvoiceCreate): Invoice creation schema.
        db (Session): SQLAlchemy session.

    Returns:
        InvoiceOut: Created invoice with HATEOAS links.

    Author: Vytautas Petronis <vytautas.petronis@stud.viko.lt>
    """
    created = crud_invoice.create_invoice(db, invoice)
    return {
        **created.__dict__,
        "links": generate_invoice_links(created.__dict__)
    }

@router.delete("/{invoice_id}", operation_id="deleteInvoice")
def delete_invoice(invoice_id: int, db: Session = Depends(get_db)):
    """
    Delete an invoice by ID.

    Args:
        invoice_id (int): Invoice identifier.
        db (Session): SQLAlchemy session.

    Returns:
        dict: Confirmation message.

    Raises:
        HTTPException: If invoice is not found.

    Author: Vytautas Petronis <vytautas.petronis@stud.viko.lt>
    """
    success = crud_invoice.delete_invoice(db, invoice_id)
    if not success:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return {"detail": "Invoice deleted"}

@router.patch("/{invoice_id}/status", response_model=InvoiceOut, operation_id="updateStatus")
def update_status(invoice_id: int, status: InvoiceStatusUpdate, db: Session = Depends(get_db)):
    """
    Update the status of an invoice.

    Args:
        invoice_id (int): Invoice identifier.
        status (InvoiceStatusUpdate): New status payload.
        db (Session): SQLAlchemy session.

    Returns:
        InvoiceOut: Updated invoice with HATEOAS links.

    Raises:
        HTTPException: If invoice is not found.

    Author: Vytautas Petronis <vytautas.petronis@stud.viko.lt>
    """
    updated = crud_invoice.update_invoice_status(db, invoice_id, status)
    if not updated:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return {
        **updated.__dict__,
        "links": generate_invoice_links(updated.__dict__)
    }
