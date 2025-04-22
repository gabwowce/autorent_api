from pydantic import BaseModel

class EmployeeOut(BaseModel):
    darbuotojo_id: int
    vardas: str
    pavarde: str
    el_pastas: str
    pareigos: str

    class Config:
        orm_mode = True

class EmployeeUpdate(BaseModel):
    vardas: str | None = None
    pavarde: str | None = None
    el_pastas: str | None = None
    pareigos: str | None = None
    telefono_nr: str | None = None
    slaptazodis: str | None = None
