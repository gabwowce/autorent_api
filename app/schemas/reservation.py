from pydantic import BaseModel
from datetime import date
from typing import List, Dict, Optional

# 1️⃣ Bendra bazė be ID ir be links
class ReservationBase(BaseModel):
    kliento_id: int
    automobilio_id: int
    rezervacijos_pradzia: date
    rezervacijos_pabaiga: date
    busena: str

# 2️⃣ Kūrimo schema (POST)
class ReservationCreate(ReservationBase):
    pass

# 3️⃣ Atnaujinimo schema (PATCH/PUT, jei reikės)
class ReservationUpdate(BaseModel):
    rezervacijos_pradzia: Optional[date] = None
    rezervacijos_pabaiga: Optional[date] = None
    busena: Optional[str] = None

# 4️⃣ Schema atsakymui į klientą (su ID ir links)
class ReservationOut(ReservationBase):
    rezervacijos_id: int
    kliento_id: int
    automobilio_id: int
    links: List[Dict]

    class Config:
        orm_mode = True

class ReservationSummary(BaseModel):
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
