"""
app/services/auth_service.py

Utility functions for password hashing and JWT token generation.

Author: Gabrielė Tamaševičiūtė <gabriele.tamaseviciute@stud.viko.lt>

Description:
    Contains helper functions for verifying and hashing passwords using passlib,
    and creating access tokens using JOSE JWT for authentication purposes.
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
    Verify a plain password against its hashed version.

    Args:
        plain_password (str): The plain text password provided by the user.
        hashed_password (str): The hashed password stored in the database.

    Returns:
        bool: True if the password matches the hash, False otherwise.

    Author: Gabrielė Tamaševičiūtė <gabriele.tamaseviciute@stud.viko.lt>
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """
    Hash a plain password using bcrypt.

    Args:
        password (str): The plain text password to hash.

    Returns:
        str: The hashed password.

    Author: Gabrielė Tamaševičiūtė <gabriele.tamaseviciute@stud.viko.lt>
    """
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    Generate a JWT access token with expiration.

    Args:
        data (dict): The data to encode inside the token.
        expires_delta (timedelta, optional): The token's expiration period.
            If not provided, defaults to ACCESS_TOKEN_EXPIRE_MINUTES.

    Returns:
        str: The encoded JWT token.

    Author: Gabrielė Tamaševičiūtė <gabriele.tamaseviciute@stud.viko.lt>
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

