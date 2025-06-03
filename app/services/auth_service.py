"""
app/services/auth_service.py

Utilities for authentication: password hashing and JWT token generation.

Author: Gabrielė Tamaševičiūtė <gabriele.tamaseviciutes@stud.viko.lt>

Description:
    Provides helper functions for:
    - Verifying and hashing passwords using bcrypt.
    - Creating access tokens (JWT) with expiration.
"""
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

SECRET_KEY = "super-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Bcrypt kontekstas slaptažodžių maišymui
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    """
    Patikrina ar įvestas slaptažodis sutampa su išsaugotu maišu.

    Args:
        plain_password (str): Nešifruotas slaptažodis.
        hashed_password (str): Maišuotas slaptažodis.

    Returns:
        bool: True, jei slaptažodžiai sutampa.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """
    Sugeneruoja maišą iš pateikto slaptažodžio.

    Args:
        password (str): Nešifruotas slaptažodis.

    Returns:
        str: Maišuotas slaptažodis.
    """
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    Sukuria JWT tokeną su galiojimo laiku.

    Args:
        data (dict): Duomenys, kurie bus įdėti į tokeną.
        expires_delta (timedelta, optional): Tokeno galiojimo trukmė.

    Returns:
        str: Užkoduotas JWT tokenas.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
