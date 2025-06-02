"""
app/schemas/invoice.py

Pydantic schemas for invoice operations in the Car Rental API.

Author: Vytautas Petronis <vytautas.petronis@stud.viko.lt>

Description:
    Defines the request and response data models for invoice-related
    API endpoints, including creation, update, and output schemas.
"""
from pydantic import BaseModel
from datetime import date
from typing import Optional, List, Dict

class InvoiceBase(BaseModel):
    """
    Base schema for invoice data (used for common invoice fields).

    Attributes:
        order_id (int): Related order identifier.
        total (float): Invoice total amount.
        invoice_date (date): Date of the invoice.

    Author: Vytautas Petronis <vytautas.petronis@stud.viko.lt>
    """
    order_id: int
    total: float
    invoice_date: date

class InvoiceCreate(InvoiceBase):
    """
    Schema for creating a new invoice.

    Inherits from:
        InvoiceBase

    Author: Vytautas Petronis <vytautas.petronis@stud.viko.lt>
    """
    pass

class InvoiceStatusUpdate(BaseModel):
    """
    Schema for updating the status of an invoice.

    Attributes:
        status (str): New status for the invoice.

    Author: Vytautas Petronis <vytautas.petronis@stud.viko.lt>
    """
    status: str

class InvoiceOut(InvoiceBase):
    """
    Schema for returning invoice information to the client, with additional fields.

    Attributes:
        invoice_id (int): Unique invoice identifier.
        order_id (int): Related order identifier.
        kliento_id (int): Client identifier.
        total (float): Invoice total amount.
        invoice_date (date): Date of the invoice.
        status (str): Invoice status.
        client_first_name (str): Client's first name.
        client_last_name (str): Client's last name.
        links (List[Dict]): HATEOAS links.

    Author: Vytautas Petronis <vytautas.petronis@stud.viko.lt>
    """
    invoice_id: int
    order_id: int
    kliento_id: int
    total: float
    invoice_date: date
    status: str
    client_first_name: str
    client_last_name: str
    links: List[Dict]

    class Config:
        orm_mode = True
