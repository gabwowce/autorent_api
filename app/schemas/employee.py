from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional, List, Dict

# 1️⃣ Bendras pagrindas – bendri laukai
class EmployeeBase(BaseModel):
    vardas: str
    pavarde: str
    el_pastas: EmailStr
    telefono_nr: Optional[str]
    pareigos: str
    atlyginimas: int
    isidarbinimo_data: date

# 2️⃣ Kūrimo schema (naudojama POST metu)
class EmployeeCreate(EmployeeBase):
    slaptazodis: str  # plaintext arba hashed vėliau

# 3️⃣ Atnaujinimo schema
class EmployeeUpdate(BaseModel):
    vardas: Optional[str] = None
    pavarde: Optional[str] = None
    el_pastas: Optional[EmailStr] = None
    telefono_nr: Optional[str] = None
    pareigos: Optional[str] = None
    atlyginimas: Optional[int] = None
    isidarbinimo_data: Optional[date] = None
    slaptazodis: Optional[str] = None

# 4️⃣ Išvedimo schema su ID ir HATEOAS nuorodomis
class EmployeeOut(EmployeeBase):
    darbuotojo_id: int
    links: List[Dict]

    class Config:
        orm_mode = True
