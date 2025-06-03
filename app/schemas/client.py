"""
app/schemas/client.py

Pydantic schemas for client-related operations in the Car Rental API.

Author: Ivan Bruner <ivan.bruner@stud.viko.lt>

Description:
    Defines data models for client base attributes, creation, update, and response
    including HATEOAS links. Used for API validation, serialization, and OpenAPI docs.
"""
from pydantic import BaseModel, EmailStr
from datetime import date,datetime
from typing import List, Dict

class ClientBase(BaseModel):
    """
    Base schema for client attributes (used in all client operations).

    Fields:
        vardas (str): Client first name.
        pavarde (str): Client last name.
        el_pastas (EmailStr): Client email address.
        telefono_nr (str): Client phone number.
        gimimo_data (date): Date of birth.
        registracijos_data (datetime): Registration date and time.
        bonus_taskai (int): Loyalty bonus points.

    Author: Ivan Bruner <ivan.bruner@stud.viko.lt>
    """
    vardas: str
    pavarde: str
    el_pastas: EmailStr
    telefono_nr: str
    gimimo_data: date
    registracijos_data: datetime
    bonus_taskai: int

class ClientCreate(ClientBase):
    """
    Schema for client creation (POST requests).

    Inherits all fields from ClientBase.

    Author: Ivan Bruner <ivan.bruner@stud.viko.lt>
    """
    pass

class ClientUpdate(ClientBase):
    """
    Schema for client update (PUT/PATCH requests).

    Inherits all fields from ClientBase.

    Author: Ivan Bruner <ivan.bruner@stud.viko.lt>
    """
    pass

class ClientOut(ClientBase):
    """
    Schema for client output/response.

    Fields:
        kliento_id (int): Client unique identifier.
        links (List[Dict]): HATEOAS links for related actions.

    Inherits all fields from ClientBase.

    Author: Ivan Bruner <ivan.bruner@stud.viko.lt>
    """
    kliento_id: int
    links: List[Dict]

    class Config:
        orm_mode = True
