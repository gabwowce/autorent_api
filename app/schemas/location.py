"""
app/schemas/location.py

Pydantic schema for returning location (delivery point) data.

Author: Gabrielė Tamaševičiūtė <gabriele.tamaseviciutes@stud.viko.lt>

Description:
    Defines the structure used when returning location details in API responses.
"""
from pydantic import BaseModel

class LocationOut(BaseModel):
    """
    Schema representing a delivery/pickup location.

    Fields:
        vietos_id (int): Unique location ID.
        pavadinimas (str): Location name.
        adresas (str): Full address.
        miestas (str): City name.
    """
    vietos_id: int
    pavadinimas: str
    adresas: str
    miestas: str

    class Config:
        orm_mode = True
