"""
app/schemas/geocode.py

Pydantic schemas for geocoding requests and responses.

Author: Gabrielė Tamaševičiūtė <gabriele.tamaseviciutes@stud.viko.lt>

Description:
    Defines the request and response structure for the geocoding endpoint.
"""
from pydantic import BaseModel

class GeocodeRequest(BaseModel):
    """
    Schema for geocoding request.

    Fields:
        adresas (str): Address to convert into geographic coordinates.
    """
    adresas: str

class GeocodeResponse(BaseModel):
    """
    Schema for geocoding response.

    Fields:
        lat (float): Latitude.
        lng (float): Longitude.
    """
    lat: float
    lng: float
