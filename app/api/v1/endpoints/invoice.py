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
    get = lambda obj, key: obj.get(key) if isinstance(obj, dict) else getattr(obj, key)
    return [
        {"rel": "self", "href": f"/invoices/{get(invoice, 'saskaitos_id')}"},
        {"rel": "order", "href": f"/orders/{get(invoice, 'uzsakymo_id')}"},
        {"rel": "update_status", "href": f"/invoices/{get(invoice, 'saskaitos_id')}/status"},
        {"rel": "delete", "href": f"/invoices/{get(invoice, 'saskaitos_id')}"}
    ]


@router.get("/", response_model=list[InvoiceOut], operation_id="getAllInvoices")
def get_all_invoices(db: Session = Depends(get_db)):
    raw_data = crud_invoice.get_invoice(db)  # tai yra sąrašas dict'ų
    return [
        {
            **invoice,
            "links": generate_invoice_links(invoice)
        }
        for invoice in raw_data
    ]

@router.post("/", response_model=InvoiceOut, operation_id="createInvoice")
def create_invoice(invoice: InvoiceCreate, db: Session = Depends(get_db)):
    created = crud_invoice.create_invoice(db, invoice)  # ORM objektas
    return {
        **created.__dict__,
        "links": generate_invoice_links(created.__dict__)  # čia jau reikia dict
    }

@router.delete("/{invoice_id}", operation_id="deleteInvoice")
def delete_invoice(invoice_id: int, db: Session = Depends(get_db)):
    success = crud_invoice.delete_invoice(db, invoice_id)
    if not success:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return {"detail": "Invoice deleted"}

@router.patch("/{invoice_id}/status", response_model=InvoiceOut, operation_id="updateStatus")
def update_status(invoice_id: int, status: InvoiceStatusUpdate, db: Session = Depends(get_db)):
    updated = crud_invoice.update_invoice_status(db, invoice_id, status)
    if not updated:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return {
        **updated.__dict__,
        "links": generate_invoice_links(updated.__dict__)
    }
