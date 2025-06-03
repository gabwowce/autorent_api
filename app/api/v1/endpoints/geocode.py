"""
app/api/v1/endpoints/geocode.py

API endpoint for converting address to geographic coordinates (geocoding).

Author: Gabrielė Tamaševičiūtė <gabriele.tamaseviciutes@stud.viko.lt>

Description:
    Provides an endpoint to retrieve latitude and longitude from an address string.
    Uses asynchronous geocoding logic and returns structured response.
"""
from fastapi import APIRouter, HTTPException
from app.schemas.geocode import GeocodeRequest, GeocodeResponse
from app.repositories.geocode import geocode_address

router = APIRouter(
    prefix="/api",
    tags=["Geo Code"]
)

@router.post("/geocode", response_model=GeocodeResponse, operation_id="geoCode")
async def geocode(req: GeocodeRequest):
    """
    Convert an address to geographic coordinates (latitude, longitude).

    Args:
        req (GeocodeRequest): Request containing the address.

    Returns:
        GeocodeResponse: Latitude and longitude coordinates.

    Raises:
        HTTPException: If coordinates not found for given address.

    Author: Gabrielė Tamaševičiūtė <gabriele.tamaseviciutes@stud.viko.lt>
    """
    coords = await geocode_address(req.adresas)

    if coords is None:
        raise HTTPException(status_code=404, detail="Koordinatės nerastos")

    lat, lng = coords
    return GeocodeResponse(lat=lat, lng=lng)
