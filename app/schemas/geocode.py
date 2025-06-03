"""
app/schemas/geocode.py

Pydantic schemas for geocoding requests and responses.

Author: Gabrielė Tamaševičiūtė <gabriele.tamaseviciute@stud.viko.lt>

Description:
    This module defines request and response schemas for geocoding API endpoints,
    allowing address-to-coordinates conversion and vice versa.

Usage:
    from schemas.geocode import GeocodeRequest, GeocodeResponse
"""
from pydantic import BaseModel, Field

class GeocodeRequest(BaseModel):
    """
    Request schema for geocoding (address-to-coordinates) operation.

    Attributes:
        adresas (str): The address to geocode.

    Author: Gabrielė Tamaševičiūtė <gabriele.tamaseviciute@stud.viko.lt>
    """
    adresas: str = Field(..., min_length=1)

class GeocodeResponse(BaseModel):
    """
    Response schema for geocoding operation.

    Attributes:
        lat (float): Latitude coordinate.
        lng (float): Longitude coordinate.

    Author: Gabrielė Tamaševičiūtė <gabriele.tamaseviciute@stud.viko.lt>
    """
    lat: float
    lng: float
