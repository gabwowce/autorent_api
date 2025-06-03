"""
app/repositories/geocode.py

Functions for address geocoding using the OpenCage API.

Author: Gabrielė Tamaševičiūtė <gabriele.tamaseviciute@stud.viko.lt>

Description:
    Provides asynchronous geocoding functionality for converting an address to latitude and longitude
    coordinates by calling the OpenCage Geocoding API.
"""
import httpx

OPENCAGE_API_KEY="f49a14ddc4414655ac28e13737621062"
async def geocode_address(adresas: str) -> tuple[float, float] | None:
    """
    Geocode a given address string to latitude and longitude coordinates using the OpenCage API.

    Args:
        adresas (str): Address to geocode.

    Returns:
        tuple[float, float] | None: Tuple with (latitude, longitude) if found, otherwise None.

    Author: Gabrielė Tamaševičiūtė <gabriele.tamaseviciute@stud.viko.lt>
    """
    query = f"{adresas}, Lietuva"
    url = f"https://api.opencagedata.com/geocode/v1/json?q={query}&key={OPENCAGE_API_KEY}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()

    if not data["results"]:
        return None

    geometry = data["results"][0]["geometry"]
    return geometry["lat"], geometry["lng"]
