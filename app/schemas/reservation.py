"""
app/schemas/reservation.py

Pydantic schemas for reservation operations in the Car Rental API.

Author: Vytautas Petronis <vytautas.petronis@stud.viko.lt>

Description:
    Defines data models for reservation creation, update, full responses,
    and reservation summary with HATEOAS support.
"""

from pydantic import BaseModel
from datetime import date
from typing import List, Dict, Optional


class ReservationBase(BaseModel):
    """
    Common base schema for reservation data.

    Attributes:
        kliento_id (int): ID of the client.
        automobilio_id (int): ID of the car.
        rezervacijos_pradzia (date): Reservation start date.
        rezervacijos_pabaiga (date): Reservation end date.
        busena (str): Status of the reservation.
    """
    kliento_id: int
    automobilio_id: int
    rezervacijos_pradzia: date
    rezervacijos_pabaiga: date
    busena: str


class ReservationCreate(ReservationBase):
    """
    Schema used for creating a new reservation.
    Inherits all fields from ReservationBase.
    """
    pass


class ReservationUpdate(BaseModel):
    """
    Schema used for partially updating a reservation.

    Attributes:
        kliento_id (Optional[int]): ID of the client.
        automobilio_id (Optional[int]): ID of the car.
        rezervacijos_pradzia (Optional[date]): New start date.
        rezervacijos_pabaiga (Optional[date]): New end date.
        busena (Optional[str]): New status.
    """
    kliento_id: Optional[int] = None
    automobilio_id: Optional[int] = None
    rezervacijos_pradzia: Optional[date] = None
    rezervacijos_pabaiga: Optional[date] = None
    busena: Optional[str] = None


class ReservationOut(ReservationBase):
    """
    Full reservation schema returned to the client.

    Attributes:
        rezervacijos_id (int): Unique identifier of the reservation.
        links (List[Dict]): HATEOAS links for navigation.
    """
    rezervacijos_id: int
    links: List[Dict]

    class Config:
        orm_mode = True


class ReservationSummary(BaseModel):
    """
    Summary schema for displaying the latest reservations with details.

    Attributes:
        rezervacijos_id (int): Unique identifier of the reservation.
        kliento_id (int): ID of the client.
        automobilio_id (int): ID of the car.
        rezervacijos_pradzia (date): Start date of the reservation.
        rezervacijos_pabaiga (date): End date of the reservation.
        busena (str): Reservation status.
        marke (str): Brand of the car.
        modelis (str): Model of the car.
        vardas (str): First name of the client.
        pavarde (str): Last name of the client.
        links (List[Dict]): HATEOAS links for frontend use.
    """
    rezervacijos_id: int
    kliento_id: int
    automobilio_id: int
    rezervacijos_pradzia: date
    rezervacijos_pabaiga: date
    busena: str
    marke: str
    modelis: str
    vardas: str
    pavarde: str
    links: List[Dict]

    class Config:
        orm_mode = True
