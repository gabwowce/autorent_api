"""
app/schemas/reservation.py

Pydantic schemas for reservation operations in the Car Rental API.

Author: Vytautas Petronis <vytautas.petronis@stud.viko.lt>

Description:
    Provides data models for reservation creation, update, API responses,
    and reservation summary views, including HATEOAS support.
"""
from pydantic import BaseModel
from datetime import date
from typing import List, Dict, Optional

class ReservationBase(BaseModel):
    """
    Base schema for reservation data.

    Attributes:
        kliento_id (int): Client identifier.
        automobilio_id (int): Car identifier.
        rezervacijos_pradzia (date): Reservation start date.
        rezervacijos_pabaiga (date): Reservation end date.
        busena (str): Reservation status.

    Author: Vytautas Petronis <vytautas.petronis@stud.viko.lt>
    """
    kliento_id: int
    automobilio_id: int
    rezervacijos_pradzia: date
    rezervacijos_pabaiga: date
    busena: str

class ReservationCreate(ReservationBase):
    """
    Schema for creating a new reservation.

    Inherits from:
        ReservationBase

    Author: Vytautas Petronis <vytautas.petronis@stud.viko.lt>
    """
    pass

class ReservationUpdate(BaseModel):
    """
    Schema for updating an existing reservation.

    Attributes:
        rezervacijos_pradzia (Optional[date]): Updated start date.
        rezervacijos_pabaiga (Optional[date]): Updated end date.
        busena (Optional[str]): Updated reservation status.

    Author: Vytautas Petronis <vytautas.petronis@stud.viko.lt>
    """
    rezervacijos_pradzia: Optional[date] = None
    rezervacijos_pabaiga: Optional[date] = None
    busena: Optional[str] = None

class ReservationOut(ReservationBase):
    """
    Schema for returning reservation information to the client.

    Attributes:
        rezervacijos_id (int): Unique reservation identifier.
        kliento_id (int): Client identifier.
        automobilio_id (int): Car identifier.
        links (List[Dict]): List of HATEOAS links.

    Author: Vytautas Petronis <vytautas.petronis@stud.viko.lt>
    """
    rezervacijos_id: int
    kliento_id: int
    automobilio_id: int
    links: List[Dict]

    class Config:
        orm_mode = True

class ReservationSummary(BaseModel):
    """
    Schema for reservation summary responses.

    Attributes:
        rezervacijos_id (int): Unique reservation identifier.
        rezervacijos_pradzia (date): Reservation start date.
        rezervacijos_pabaiga (date): Reservation end date.
        marke (str): Car brand.
        modelis (str): Car model.
        vardas (str): Client's first name.
        pavarde (str): Client's last name.
        links (List[Dict]): List of HATEOAS links.

    Author: Vytautas Petronis <vytautas.petronis@stud.viko.lt>
    """
    rezervacijos_id: int
    rezervacijos_pradzia: date
    rezervacijos_pabaiga: date
    marke: str
    modelis: str
    vardas: str
    pavarde: str
    links: List[Dict]

    class Config:
        orm_mode = True
