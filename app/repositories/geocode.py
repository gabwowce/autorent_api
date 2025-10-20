import httpx

OPENCAGE_API_KEY="55ec8b9f6e94477aacf95fd41b9fc808"
async def geocode_address(adresas: str) -> tuple[float, float] | None:
    query = f"{adresas}, Lietuva"
    url = f"https://api.opencagedata.com/geocode/v1/json?q={query}&key={OPENCAGE_API_KEY}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()

    if not data["results"]:
        return None

    geometry = data["results"][0]["geometry"]
    return geometry["lat"], geometry["lng"]
