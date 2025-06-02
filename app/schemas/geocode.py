from pydantic import BaseModel

class GeocodeRequest(BaseModel):
    adresas: str

class GeocodeResponse(BaseModel):
    lat: float
    lng: float
