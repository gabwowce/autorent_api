"""
app/repositories/invoice.py

Repository functions for Invoice entity database operations.

Author: Vytautas Petronis <vytautas.petronis@stud.viko.lt>

Description:
    Provides CRUD operations and utility queries for Invoice objects using SQLAlchemy.
"""
from sqlalchemy.orm import Session
from app.models.invoice import Invoice
from app.models.order import Order
from app.models import client as klientas_model
from app.schemas.invoice import InvoiceCreate, InvoiceStatusUpdate
from datetime import datetime

def get_invoice(db: Session):
    """
    Retrieve all invoice records with related order and client information.

    Args:
        db (Session): SQLAlchemy session.

    Returns:
        List[dict]: List of invoice records with detailed fields.

    Author: Vytautas Petronis <vytautas.petronis@stud.viko.lt>
    """
    query = (
        db.query(
            Invoice.saskaitos_id.label("invoice_id"),
            Invoice.uzsakymo_id.label("order_id"),
            Order.kliento_id.label("kliento_id"),
            Invoice.suma.label("total"),
            Invoice.saskaitos_data.label("invoice_date"),
            Order.uzsakymo_busena.label("status"),
            klientas_model.Client.vardas.label("client_first_name"),
            klientas_model.Client.pavarde.label("client_last_name"),
        )
        .join(Order, Invoice.uzsakymo_id == Order.uzsakymo_id)
        .join(klientas_model.Client, Order.kliento_id == klientas_model.Client.kliento_id)
    )

    results = query.all()
    keys = [col['name'] for col in query.column_descriptions]
    invoices = []
    for row in results:
        d = dict(zip(keys, row))
        # Paversk jei reikia
        if isinstance(d["invoice_date"], datetime):
            d["invoice_date"] = d["invoice_date"].date()
        invoices.append(d)
    return invoices




def create_invoice(db: Session, invoice_data: InvoiceCreate):
    """
    Create a new invoice record in the database.

    Args:
        db (Session): SQLAlchemy session.
        invoice_data (InvoiceCreate): Pydantic schema with invoice data.

    Returns:
        Invoice: The created invoice object.

    Author: Vytautas Petronis <vytautas.petronis@stud.viko.lt>
    """
    data = invoice_data.dict()
    invoice = Invoice(
        uzsakymo_id=data["order_id"],
        suma=data["total"],
        saskaitos_data=data["invoice_date"]
    )
    db.add(invoice)
    db.commit()
    db.refresh(invoice)
    return invoice


def delete_invoice(db: Session, invoice_id: int):
    """
    Delete an invoice record from the database.

    Args:
        db (Session): SQLAlchemy session.
        invoice_id (int): Invoice ID.

    Returns:
        bool: True if deleted successfully, False if not found.

    Author: Vytautas Petronis <vytautas.petronis@stud.viko.lt>
    """
    invoice = db.query(Invoice).filter(Invoice.saskaitos_id == invoice_id).first()
    if invoice:
        db.delete(invoice)
        db.commit()
        return True
    return False


def update_invoice_status(db: Session, invoice_id: int, status_data: InvoiceStatusUpdate):
    """
    Update the status of an invoice.

    Args:
        db (Session): SQLAlchemy session.
        invoice_id (int): Invoice ID.
        status_data (InvoiceStatusUpdate): Pydantic schema with new status.

    Returns:
        Invoice or None: Updated invoice object if found, otherwise None.

    Author: Vytautas Petronis <vytautas.petronis@stud.viko.lt>
    """
    invoice = db.query(Invoice).filter(Invoice.saskaitos_id == invoice_id).first()
    if invoice:
        order = db.query(Order).filter(Order.uzsakymo_id == invoice.uzsakymo_id).first()
        if order:
            order.uzsakymo_busena = status_data.status
            db.commit()
            db.refresh(order)
        db.refresh(invoice)
        return invoice
    return None
