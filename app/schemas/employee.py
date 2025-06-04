"""
app/schemas/employee.py

Pydantic schemas for employee-related operations in the Car Rental API.

Author: Astijus Grinevičius <astijus.grinevicius@stud.viko.lt>

Description:
    Defines data models for employee base attributes, creation, update, and API responses,
    including HATEOAS links. Used for API request validation, response serialization, and OpenAPI documentation.
"""
from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional, List, Dict

class EmployeeBase(BaseModel):
    """
    Base schema for employee attributes (common to all employee operations).

    Fields:
        vardas (str): Employee first name.
        pavarde (str): Employee last name.
        el_pastas (EmailStr): Employee email address.
        telefono_nr (Optional[str]): Employee phone number.
        pareigos (str): Position or job title.
        atlyginimas (int): Salary.
        isidarbinimo_data (date): Employment start date.

    Author: Astijus Grinevičius <astijus.grinevicius@stud.viko.lt>
    """
    vardas: str
    pavarde: str
    el_pastas: EmailStr
    telefono_nr: Optional[str]
    pareigos: str
    atlyginimas: float
    isidarbinimo_data: date

class EmployeeCreate(EmployeeBase):
    """
    Schema for creating a new employee (POST requests).

    Inherits all fields from EmployeeBase.

    Fields:
        slaptazodis (str): Plaintext or hashed password.

    Author: Astijus Grinevičius <astijus.grinevicius@stud.viko.lt>
    """
    slaptazodis: str  # plaintext arba hashed vėliau

class EmployeeUpdate(BaseModel):
    """
    Schema for updating an employee (PUT/PATCH requests).

    All fields are optional for partial updates.

    Fields:
        vardas (Optional[str]): First name.
        pavarde (Optional[str]): Last name.
        el_pastas (Optional[EmailStr]): Email address.
        telefono_nr (Optional[str]): Phone number.
        pareigos (Optional[str]): Position or job title.
        atlyginimas (Optional[int]): Salary.
        isidarbinimo_data (Optional[date]): Employment start date.
        slaptazodis (Optional[str]): Password.

    Author: Astijus Grinevičius <astijus.grinevicius@stud.viko.lt>
    """
    vardas: Optional[str] = None
    pavarde: Optional[str] = None
    el_pastas: Optional[EmailStr] = None
    telefono_nr: Optional[str] = None
    pareigos: Optional[str] = None
    atlyginimas: Optional[float] = None
    isidarbinimo_data: Optional[date] = None
    slaptazodis: Optional[str] = None

class EmployeeOut(EmployeeBase):
    """
    Schema for employee output/response.

    Fields:
        darbuotojo_id (int): Employee unique identifier.
        links (List[Dict]): HATEOAS links for related actions.

    Inherits all fields from EmployeeBase.

    Author: Astijus Grinevičius <astijus.grinevicius@stud.viko.lt>
    """
    darbuotojo_id: int
    links: List[Dict]

    class Config:
        orm_mode = True

