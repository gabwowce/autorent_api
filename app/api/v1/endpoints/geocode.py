"""
app/api/v1/endpoints/geocode.py

API endpoint for geocoding address requests.

Author: Gabrielė Tamaševičiūtė <gabriele.tamaseviciute@stud.viko.lt>

Description:
    Implements an endpoint for geocoding addresses into latitude and longitude using an external geocoding service.
    Receives an address in the request body and returns coordinates as a response.

Usage:
    Register this router with the main FastAPI app to enable /api/geocode POST endpoint.
"""
from fastapi import APIRouter, HTTPException
from app.schemas.geocode import GeocodeRequest, GeocodeResponse
from app.repositories.geocode import geocode_address

router = APIRouter(tags=["Geo Code"])

@router.post("/geocode", response_model=GeocodeResponse, operation_id="geoCode")
async def geocode(req: GeocodeRequest):
    """
    Convert an address to latitude and longitude coordinates.

    Args:
        req (GeocodeRequest): Request body containing the address string.

    Returns:
        GeocodeResponse: The latitude and longitude if found.

    Raises:
        HTTPException: If coordinates are not found for the provided address.

    Author: Gabrielė Tamaševičiūtė <gabriele.tamaseviciute@stud.viko.lt>
    """
    coords = await geocode_address(req.adresas)

    if coords is None:
        raise HTTPException(status_code=404, detail="Koordinatės nerastos")

    lat, lng = coords
    return GeocodeResponse(lat=lat, lng=lng)
