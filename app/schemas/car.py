"""
app/schemas/car.py

Pydantic schemas for car-related data validation and serialization.

Author: Gabrielė Tamaševičiūtė <gabriele.tamaseviciutes@stud.viko.lt>

Description:
    Contains schemas for creating, updating, and returning car data,
    including optional location info and HATEOAS links.
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import date

from app.schemas.location import LocationOut

# 1️⃣ Bendras pagrindas visoms schemoms
class CarBase(BaseModel):
    """
    Common fields shared by all car schemas.
    All fields are optional for reuse flexibility.
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

# 2️⃣ Kūrimo schema (naudojama POST metu)
class CarCreate(CarBase):
    """
    Schema for creating a new car.

    Inherits all fields from CarBase.
    """
    pass

# 3️⃣ Atnaujinimo schema (naudojama PUT/PATCH metu)
class CarUpdate(CarBase):
    """
    Schema for updating an existing car.

    All fields are optional, partial updates supported.
    """
    pass

class CarOut(CarBase):
    """
    Schema used when returning car data to the client.

    Fields:
        automobilio_id (int): Unique car ID.
        lokacija (LocationOut | None): Optional location info.
        links (list[dict]): HATEOAS-style navigation links.
    """
    automobilio_id: int
    lokacija: Optional[LocationOut]
    links: List[dict]

    class Config:
        orm_mode = True

class CarStatusUpdate(BaseModel):
    """
    Schema used to update only the status of a car.

    Fields:
        status (str): New car status.
    """
    status: str
