"""
app/schemas/car.py

Pydantic schemas for car-related operations in the Car Rental API.

Author: Gabrielė Tamaševičiūtė <gabriele.tamaseviciute@stud.viko.lt>

Description:
    Provides data models for car base attributes, creation, update, output, and status changes.
    Used for API request validation, response serialization, and OpenAPI documentation.
"""
from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import date

from app.schemas.location import LocationOut

class CarBase(BaseModel):
    """
    Base schema for car attributes (common to all car operations).

    Fields:
        marke (str): Car brand.
        modelis (str): Car model.
        metai (int): Year of manufacture.
        numeris (str): License plate number.
        vin_kodas (str): VIN code.
        spalva (str): Color.
        kebulo_tipas (str): Body type.
        pavarų_deze (str): Gearbox type.
        variklio_turis (float): Engine capacity (L).
        galia_kw (int): Engine power (kW).
        kuro_tipas (str): Fuel type.
        rida (int): Odometer reading (km).
        sedimos_vietos (int): Number of seats.
        klimato_kontrole (bool): Has climate control.
        navigacija (bool): Has navigation.
        kaina_parai (float): Price per day.
        automobilio_statusas (str): Car status (e.g., 'laisvas').
        technikines_galiojimas (date): Technical inspection expiry.
        dabartine_vieta_id (int): Current location ID.
        pastabos (Optional[str]): Additional notes.

    Author: Gabrielė Tamaševičiūtė <gabriele.tamaseviciute@stud.viko.lt>
    """
    marke: str
    modelis: str
    metai: int
    numeris: str
    vin_kodas: str
    spalva: str
    kebulo_tipas: str
    pavarų_deze: str
    variklio_turis: float
    galia_kw: int
    kuro_tipas: str
    rida: int
    sedimos_vietos: int
    klimato_kontrole: bool
    navigacija: bool
    kaina_parai: float
    automobilio_statusas: str
    technikines_galiojimas: date
    dabartine_vieta_id: int
    pastabos: Optional[str]

class CarCreate(CarBase):
    """
    Schema for car creation (POST requests).

    Inherits all fields from CarBase.

    Author: Gabrielė Tamaševičiūtė <gabriele.tamaseviciute@stud.viko.lt>
    """
    pass

class CarUpdate(BaseModel):
    """
    Schema for car update (PUT/PATCH requests).

    All fields optional to allow partial updates.

    Author: Gabrielė Tamaševičiūtė <gabriele.tamaseviciute@stud.viko.lt>
    """
    marke: Optional[str] = None
    modelis: Optional[str] = None
    metai: Optional[int] = None
    numeris: Optional[str] = None
    vin_kodas: Optional[str] = None
    spalva: Optional[str] = None
    kebulo_tipas: Optional[str] = None
    pavarų_deze: Optional[str] = None
    variklio_turis: Optional[float] = None
    galia_kw: Optional[int] = None
    kuro_tipas: Optional[str] = None
    rida: Optional[int] = None
    sedimos_vietos: Optional[int] = None
    klimato_kontrole: Optional[bool] = None
    navigacija: Optional[bool] = None
    kaina_parai: Optional[float] = None
    automobilio_statusas: Optional[str] = None
    technikines_galiojimas: Optional[date] = None
    dabartine_vieta_id: Optional[int] = None
    pastabos: Optional[str] = None

    class Config:
        orm_mode = True

class CarOut(CarBase):
    """
    Schema for car output (response model).

    Fields:
        automobilio_id (int): Car unique identifier.
        lokacija (Optional[LocationOut]): Detailed location info.
        links (List[dict]): HATEOAS links for related actions.

    Inherits all fields from CarBase.

    Author: Gabrielė Tamaševičiūtė <gabriele.tamaseviciute@stud.viko.lt>
    """
    automobilio_id: int
    lokacija: Optional[LocationOut]
    links: List[Dict]

    class Config:
        orm_mode = True

class CarStatusUpdate(BaseModel):
    """
    Schema for car status update requests.

    Fields:
        status (str): New car status.

    Author: Gabrielė Tamaševičiūtė <gabriele.tamaseviciute@stud.viko.lt>
    """
    status: str
