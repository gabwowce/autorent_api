"""
app/schemas/client_support.py

Pydantic schemas for client support operations in the Car Rental API.

Author: Ivan Bruner <ivan.bruner@stud.viko.lt>

Description:
    Defines data models for client support requests, creation, update, and API responses
    with HATEOAS links. Used for API validation, serialization, and OpenAPI documentation.
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Dict

class ClientSupportBase(BaseModel):
    """
    Base schema for client support attributes.

    Fields:
        kliento_id (int): ID of the client who submitted the support request.
        darbuotojo_id (int): ID of the employee handling the request.
        tema (str): Topic of the request.
        pranesimas (str): The message sent by the client.
        atsakymas (Optional[str]): The employee's response message.
        pateikimo_data (datetime): Date/time the request was submitted.
        atsakymo_data (Optional[datetime]): Date/time the request was answered.

    Author: Ivan Bruner <ivan.bruner@stud.viko.lt>
    """
    kliento_id: int
    darbuotojo_id: int
    tema: str
    pranesimas: str
    atsakymas: Optional[str] = None
    pateikimo_data: datetime
    atsakymo_data: Optional[datetime] = None

class ClientSupportCreate(ClientSupportBase):
    """
    Schema for creating a new client support request.

    Inherits all fields from ClientSupportBase.

    Author: Ivan Bruner <ivan.bruner@stud.viko.lt>
    """
    pass

class ClientSupportUpdate(BaseModel):
    """
    Schema for updating a client support request (response/answer).

    Fields:
        atsakymas (Optional[str]): The employee's response message.
        atsakymo_data (Optional[datetime]): Date/time the request was answered.

    Author: Ivan Bruner <ivan.bruner@stud.viko.lt>
    """
    atsakymas: Optional[str]
    atsakymo_data: Optional[datetime]

class ClientSupportOut(ClientSupportBase):
    """
    Schema for API response with support request details and HATEOAS links.

    Fields:
        uzklausos_id (int): Unique ID of the support request.
        links (List[Dict]): HATEOAS links for related actions.

    Inherits all fields from ClientSupportBase.

    Author: Ivan Bruner <ivan.bruner@stud.viko.lt>
    """
    uzklausos_id: int
    links: List[Dict]

    class Config:
        orm_mode = True
