from sqlalchemy.orm import Session
from app.models.invoice import Invoice
from app.models.order import Order
from app.models import client as klientas_model
from app.schemas.invoice import InvoiceCreate, InvoiceStatusUpdate

def get_invoice(db: Session):
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

    # Taisytas: iš dict ištraukiam 'name' raktą
    keys = [col['name'] for col in query.column_descriptions]
    return [dict(zip(keys, row)) for row in results]




def create_invoice(db: Session, invoice_data: InvoiceCreate):
    invoice = Invoice(**invoice_data.dict())
    db.add(invoice)
    db.commit()
    db.refresh(invoice)
    return invoice


def delete_invoice(db: Session, invoice_id: int):
    invoice = db.query(Invoice).filter(Invoice.saskaitos_id == invoice_id).first()
    if invoice:
        db.delete(invoice)
        db.commit()
        return True
    return False


def update_invoice_status(db: Session, invoice_id: int, status_data: InvoiceStatusUpdate):
    invoice = db.query(Invoice).filter(Invoice.saskaitos_id == invoice_id).first()
    if invoice:
        invoice.status = status_data.status
        db.commit()
        db.refresh(invoice)
        return invoice
    return None
