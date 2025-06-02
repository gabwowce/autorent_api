from pydantic import BaseModel

class LocationOut(BaseModel):
    vietos_id: int
    pavadinimas: str
    adresas: str
    miestas: str

    class Config:
        orm_mode = True
