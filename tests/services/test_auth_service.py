"""
Unit tests for authentication service (auth_service.py).

Author: Vytautas Petronis <vytautas.petronis@stud.viko.lt>

Description:
    Unit tests for the authentication service layer, covering:
    - get_password_hash, verify_password, create_access_token, decode_access_token
    - Edge cases: invalid password, invalid/expired JWT token

Usage:
    pytest tests/services/test_auth_service.py

Notes:
    - Import all functions/classes according to your project structure!
"""

import pytest
from app.services import auth_service
from jose import jwt

SECRET_KEY = "super-secret-key"
ALGORITHM = "HS256"

def test_password_hash_and_verify():
    """
    Tests password hashing and verification (success case).
    Verifies that the hashed password is not the same as the raw password,
    and that verify_password returns True for the correct password.
    """
    password = "SlaptasTestas!@#"
    hashed = auth_service.get_password_hash(password)
    assert isinstance(hashed, str)
    assert hashed != password
    assert auth_service.verify_password(password, hashed)

def test_verify_password_fail():
    """
    Tests password verification with a wrong password.
    Expects verify_password to return False when the password is incorrect.
    """
    password = "SlaptasTestas!@#"
    wrong_password = "blogas"
    hashed = auth_service.get_password_hash(password)
    assert not auth_service.verify_password(wrong_password, hashed)

def test_create_access_token_and_decode():
    """
    Tests JWT token creation and manual decoding using jose.jwt.
    Verifies that the created token can be decoded and the payload matches the input data.
    Does not use auth_service.decode_access_token.
    """
    user_data = {"sub": "test@viko.lt", "role": "employee"}
    token = auth_service.create_access_token(user_data)
    assert isinstance(token, str)
    # Dekoduojam ranka, be auth_service.decode_access_token
    decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert decoded["sub"] == user_data["sub"]
    assert decoded["role"] == user_data["role"]

def test_decode_access_token_invalid():
    """
    Tests decoding of an invalid JWT token (should raise an exception or return None).
    Expects auth_service.decode_access_token to raise an exception for an invalid token.
    """
    bad_token = "this.is.not.a.jwt"
    with pytest.raises(Exception):
        auth_service.decode_access_token(bad_token)

def test_decode_access_token_expired(monkeypatch):
    """
    Tests decoding of an expired JWT token.
    Expects auth_service.decode_access_token to raise an exception for an expired token.
    """
    import datetime
    # Sukuria tokeną su pasibaigusia galiojimo data
    user_data = {"sub": "test@viko.lt", "role": "employee"}
    # Overwrite "expires_delta" į praeitį
    token = auth_service.create_access_token(user_data, expires_delta=datetime.timedelta(seconds=-1))
    with pytest.raises(Exception):
        auth_service.decode_access_token(token)