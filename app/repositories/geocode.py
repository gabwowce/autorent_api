"""
app/repositories/geocode.py

Asynchronous utility for converting addresses into geographic coordinates using OpenCage API.

Author: Gabrielė Tamaševičiūtė <gabriele.tamaseviciutes@stud.viko.lt>

Description:
    Provides an async function to geocode a given address and return its latitude and longitude.
    Appends "Lietuva" to the query to ensure localized accuracy.
"""
import httpx

OPENCAGE_API_KEY = "f49a14ddc4414655ac28e13737621062"

async def geocode_address(adresas: str) -> tuple[float, float] | None:
    """
    Geocode a given address using OpenCage API.

    Args:
        adresas (str): Address to geocode.

    Returns:
        tuple[float, float] | None: (latitude, longitude) or None if not found.

    Author: Gabrielė Tamaševičiūtė <gabriele.tamaseviciutes@stud.viko.lt>
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
