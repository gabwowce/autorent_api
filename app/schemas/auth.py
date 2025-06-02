from pydantic import BaseModel
from datetime import date

class LoginRequest(BaseModel):
    el_pastas: str
    slaptazodis: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class RegisterRequest(BaseModel):
    vardas: str
    pavarde: str
    el_pastas: str
    telefono_nr: str
    pareigos: str
    atlyginimas: float
    isidarbinimo_data: date
    slaptazodis: str

class UserInfo(BaseModel):
    vardas: str
    pavarde: str
    telefono_nr: str
    el_pastas: str
    pareigos: str
    isidarbinimo_data: date
    
class ChangePasswordRequest(BaseModel):
    senas_slaptazodis: str
    naujas_slaptazodis: str
