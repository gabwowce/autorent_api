"""
app/schemas/order.py

Pydantic schemas for order operations in the Car Rental API.

Author: Astijus Grinevičius <astijus.grinevicius@stud.viko.lt>

Description:
    Contains data models for order creation, update, and output in the API,
    including support for HATEOAS links.
"""
from pydantic import BaseModel, field_validator
from datetime import date
from typing import List, Dict, Optional
from decimal import Decimal

class OrderBase(BaseModel):
    """
    Base schema for order data (common order fields).

    Attributes:
        kliento_id (int): Identifier for the client placing the order.
        automobilio_id (int): Identifier for the rented car.
        darbuotojo_id (int): Identifier for the handling employee.
        nuomos_data (date): Date when the rental starts.
        grazinimo_data (date): Date when the rental ends.
        paemimo_vietos_id (int): Identifier for the pick-up location.
        grazinimo_vietos_id (int): Identifier for the drop-off location.
        bendra_kaina (int): Total price for the order.
        uzsakymo_busena (str): Current status of the order.
        turi_papildomas_paslaugas (bool): Indicates if there are additional services.

    Author: Astijus Grinevičius <astijus.grinevicius@stud.viko.lt>
    """
    kliento_id: int
    automobilio_id: int
    darbuotojo_id: int
    nuomos_data: date
    grazinimo_data: date
    paemimo_vietos_id: int
    grazinimo_vietos_id: int
    bendra_kaina: float
    uzsakymo_busena: str
    turi_papildomas_paslaugas: bool

class OrderCreate(OrderBase):
    """
    Schema for creating a new order.

    Inherits from:
        OrderBase

    Author: Astijus Grinevičius <astijus.grinevicius@stud.viko.lt>
    """
    pass

class OrderUpdate(BaseModel):
    """
    Schema for updating an existing order.

    Attributes:
        uzsakymo_busena (Optional[str]): Updated status of the order.
        grazinimo_data (Optional[date]): Updated rental end date.
        turi_papildomas_paslaugas (Optional[bool]): Updated flag for additional services.

    Author: Astijus Grinevičius <astijus.grinevicius@stud.viko.lt>
    """
    uzsakymo_busena: Optional[str]  = None
    grazinimo_data: Optional[date]  = None
    turi_papildomas_paslaugas: Optional[bool]  = None

class OrderOut(OrderBase):
    """
    Schema for returning order information to the client, with additional fields.

    Attributes:
        uzsakymo_id (int): Unique identifier for the order.
        kliento_id (int): Identifier for the client.
        automobilio_id (int): Identifier for the car.
        links (List[Dict]): List of HATEOAS links for related resources.

    Author: Astijus Grinevičius <astijus.grinevicius@stud.viko.lt>
    """
    uzsakymo_id: int
    kliento_id: int
    automobilio_id: int
    links: List[Dict]

    class Config:
        from_attributes = True
