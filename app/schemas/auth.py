"""
app/schemas/auth.py

Pydantic schemas for authentication and user-related requests and responses.

Author: Gabrielė Tamaševičiūtė <gabriele.tamaseviciute@stud.viko.lt>

Description:
    Contains data models for login, registration, token responses, user info,
    and password change operations, used for API validation and serialization.
"""
from pydantic import BaseModel
from datetime import date

class LoginRequest(BaseModel):
    """
    Schema for user login request.

    Fields:
        el_pastas (str): User email address.
        slaptazodis (str): User password.

    Author: Gabrielė Tamaševičiūtė <gabriele.tamaseviciute@stud.viko.lt>
    """
    el_pastas: str
    slaptazodis: str

class TokenResponse(BaseModel):
    """
    Schema for JWT access token response.

    Fields:
        access_token (str): JWT token string.
        token_type (str): Token type (default: 'bearer').

    Author: Gabrielė Tamaševičiūtė <gabriele.tamaseviciute@stud.viko.lt>
    """
    access_token: str
    token_type: str = "bearer"

class RegisterRequest(BaseModel):
    """
    Schema for user registration request.

    Fields:
        vardas (str): First name.
        pavarde (str): Last name.
        el_pastas (str): Email address.
        telefono_nr (str): Phone number.
        pareigos (str): Position/job title.
        atlyginimas (float): Salary.
        isidarbinimo_data (date): Employment start date.
        slaptazodis (str): Password.

    Author: Gabrielė Tamaševičiūtė <gabriele.tamaseviciute@stud.viko.lt>
    """
    vardas: str
    pavarde: str
    el_pastas: str
    telefono_nr: str
    pareigos: str
    atlyginimas: float
    isidarbinimo_data: date
    slaptazodis: str

class UserInfo(BaseModel):
    """
    Schema for user profile information response.

    Fields:
        vardas (str): First name.
        pavarde (str): Last name.
        telefono_nr (str): Phone number.
        el_pastas (str): Email address.
        pareigos (str): Position/job title.
        isidarbinimo_data (date): Employment start date.

    Author: Gabrielė Tamaševičiūtė <gabriele.tamaseviciute@stud.viko.lt>
    """
    vardas: str
    pavarde: str
    telefono_nr: str
    el_pastas: str
    pareigos: str
    isidarbinimo_data: date
    
class ChangePasswordRequest(BaseModel):
    """
    Schema for user password change request.

    Fields:
        senas_slaptazodis (str): Old password.
        naujas_slaptazodis (str): New password.

    Author: Gabrielė Tamaševičiūtė <gabriele.tamaseviciute@stud.viko.lt>
    """
    senas_slaptazodis: str
    naujas_slaptazodis: str
