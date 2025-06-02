from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import date

from app.schemas.location import LocationOut

# 1️⃣ Bendras pagrindas visoms schemoms
class CarBase(BaseModel):
    marke:                 Optional[str]   = None
    modelis:               Optional[str]   = None
    metai:                 Optional[int]   = None
    numeris:               Optional[str]   = None
    vin_kodas:             Optional[str]   = None
    spalva:                Optional[str]   = None
    kebulo_tipas:          Optional[str]   = None
    pavarų_deze:           Optional[str]   = None
    variklio_turis:        Optional[float]   = None
    galia_kw:              Optional[int]   = None
    kuro_tipas:            Optional[str]   = None
    rida:                  Optional[int]   = None
    sedimos_vietos:        Optional[int]   = None
    klimato_kontrole:      Optional[bool]  = None
    navigacija:           Optional[bool]  = None
    kaina_parai:           Optional[float] = None
    automobilio_statusas: Optional[str]   = None
    technikines_galiojimas: Optional[date] = None
    dabartine_vieta_id:    Optional[int]   = None
    pastabos:              Optional[str]   = None

# 2️⃣ Kūrimo schema (naudojama POST metu)
class CarCreate(CarBase):
    pass

# 3️⃣ Atnaujinimo schema (naudojama PUT/PATCH metu)
class CarUpdate(CarBase):
    pass

class CarOut(CarBase):
    automobilio_id: int
    lokacija: Optional[LocationOut]
    links: List[dict]

    class Config:
        orm_mode = True

class CarStatusUpdate(BaseModel):
    status: str