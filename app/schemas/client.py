from pydantic import BaseModel, EmailStr
from datetime import date,datetime
from typing import List, Dict

# 1️⃣ Bendri laukai (tėvinė schema)
class ClientBase(BaseModel):
    vardas: str
    pavarde: str
    el_pastas: EmailStr
    telefono_nr: str
    gimimo_data: date
    registracijos_data: datetime
    bonus_taskai: int

# 2️⃣ Schema kurti naujam klientui
class ClientCreate(ClientBase):
    pass

# 3️⃣ Schema atnaujinimui (jei norėsi PUT/PATCH)
class ClientUpdate(ClientBase):
    pass

# 4️⃣ Schema atsakymams (su ID ir links)
class ClientOut(ClientBase):
    kliento_id: int
    links: List[Dict]

    class Config:
        orm_mode = True
