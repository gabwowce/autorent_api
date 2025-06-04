"""
app/schemas/location.py

Pydantic schema for representing a location object.

Author: Gabrielė Tamaševičiūtė <gabriele.tamaseviciute@stud.viko.lt>

Description:
    Defines the response model for location data returned by the API.
"""
from pydantic import BaseModel

class LocationOut(BaseModel):
    """
    Response schema for location data.

    Attributes:
        vietos_id (int): Unique identifier for the location.
        pavadinimas (str): Name of the location.
        adresas (str): Address of the location.
        miestas (str): City where the location is situated.

    Author: Gabrielė Tamaševičiūtė <gabriele.tamaseviciute@stud.viko.lt>
    """
    vietos_id: int
    pavadinimas: str
    adresas: str
    miestas: str

    class Config:
        orm_mode = True
