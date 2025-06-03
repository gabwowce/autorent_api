"""
app/schemas/auth.py

Pydantic schemas for authentication and employee account management.

Author: Gabrielė Tamaševičiūtė <gabriele.tamaseviciutes@stud.viko.lt>

Description:
    Contains request and response models for:
    - Login
    - Registration
    - Authenticated user info
    - Password change
"""
from pydantic import BaseModel
from datetime import date

class LoginRequest(BaseModel):
    """
    Schema for login request.

    Fields:
        el_pastas (str): Employee email.
        slaptazodis (str): Raw password.
    """
    el_pastas: str
    slaptazodis: str

class TokenResponse(BaseModel):
    """
    Schema for successful authentication response.

    Fields:
        access_token (str): JWT token.
        token_type (str): Token type, default "bearer".
    """
    access_token: str
    token_type: str = "bearer"

class RegisterRequest(BaseModel):
    """
    Schema for employee registration request.

    Fields:
        vardas (str): First name.
        pavarde (str): Last name.
        el_pastas (str): Email.
        telefono_nr (str): Phone number.
        pareigos (str): Job title.
        atlyginimas (float): Salary.
        isidarbinimo_data (date): Employment date.
        slaptazodis (str): Raw password.
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
    Schema for returning current authenticated user info.

    Fields:
        vardas (str)
        pavarde (str)
        telefono_nr (str)
        el_pastas (str)
        pareigos (str)
        isidarbinimo_data (date)
    """
    vardas: str
    pavarde: str
    telefono_nr: str
    el_pastas: str
    pareigos: str
    isidarbinimo_data: date

class ChangePasswordRequest(BaseModel):
    """
    Schema for password change request.

    Fields:
        senas_slaptazodis (str): Current password.
        naujas_slaptazodis (str): New password.
    """
    senas_slaptazodis: str
    naujas_slaptazodis: str
