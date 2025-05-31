from pydantic import BaseModel
from datetime import date
from typing import List, Dict, Optional

# 1️⃣ Bendra bazinė schema – tik bendri laukeliai
class OrderBase(BaseModel):
    kliento_id: int
    automobilio_id: int
    darbuotojo_id: int
    nuomos_data: date
    grazinimo_data: date
    paemimo_vietos_id: int
    grazinimo_vietos_id: int
    bendra_kaina: int
    uzsakymo_busena: str
    turi_papildomas_paslaugas: bool

# 2️⃣ Naudojama POST /orders
class OrderCreate(OrderBase):
    pass

# 3️⃣ Naudojama PUT/PATCH /orders/{id} (jei darysi)
class OrderUpdate(BaseModel):
    uzsakymo_busena: Optional[str]
    grazinimo_data: Optional[date]
    turi_papildomas_paslaugas: Optional[bool]

# 4️⃣ Naudojama atsakymams (su ID ir HATEOAS)
class OrderOut(OrderBase):
    uzsakymo_id: int
    kliento_id: int
    automobilio_id: int
    links: List[Dict]

    class Config:
        orm_mode = True
