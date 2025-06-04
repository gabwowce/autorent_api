"""
app/schemas/reservationSummary.py

Pydantic schema for reservation summary responses.

Author: Vytautas Petronis <vytautas.petronis@stud.viko.lt>

Description:
    Defines the response model for reservation summary information,
    including reservation details, client, and car info with HATEOAS links.
"""
class ReservationSummary(BaseModel):
    """
    Schema for reservation summary data returned by the API.

    Attributes:
        rezervacijos_id (int): Unique reservation identifier.
        rezervacijos_pradzia (date): Reservation start date.
        rezervacijos_pabaiga (date): Reservation end date.
        marke (str): Car brand.
        modelis (str): Car model.
        vardas (str): Client's first name.
        pavarde (str): Client's last name.
        links (List[Dict]): List of HATEOAS links for related resources.

    Author: Vytautas Petronis <vytautas.petronis@stud.viko.lt>
    """
    rezervacijos_id: int
    rezervacijos_pradzia: date
    rezervacijos_pabaiga: date
    marke: str
    modelis: str
    vardas: str
    pavarde: str
    links: List[Dict]

    class Config:
        orm_mode = True
