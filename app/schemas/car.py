from pydantic import BaseModel
from typing import Optional
from datetime import date

class CarOut(BaseModel):
    automobilio_id: int
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

    class Config:
        orm_mode = True

class CarCreate(BaseModel):
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

class CarUpdate(CarCreate):
    pass

class CarStatusUpdate(BaseModel):
    status: str