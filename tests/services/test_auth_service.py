"""
Service tests for Auth (Autentikacijos servisai)

Author: Vytautas Petronis <vytautas.petronis@stud.viko.lt>

Description:
    Unit testai auth_service sluoksniui:
    - get_password_hash, verify_password, create_access_token, decode_access_token
    - Edge-case: blogas slaptažodis, blogas/expired JWT tokenas

Usage:
    pytest tests/services/test_auth_service.py

Pastabos:
    - Importuok funkcijas/klases pagal savo projekto struktūrą!
"""

import pytest
from app.services import auth_service

def test_password_hash_and_verify():
    """
    Testuoja slaptažodžio hashinimą ir verifikavimą (sėkmės atvejis).
    """
    password = "SlaptasTestas!@#"
    hashed = auth_service.get_password_hash(password)
    assert isinstance(hashed, str)
    assert hashed != password
    assert auth_service.verify_password(password, hashed)

def test_verify_password_fail():
    """
    Testuoja neteisingą slaptažodį (turi grąžinti False).
    """
    password = "SlaptasTestas!@#"
    wrong_password = "blogas"
    hashed = auth_service.get_password_hash(password)
    assert not auth_service.verify_password(wrong_password, hashed)

def test_create_access_token_and_decode():
    """
    Testuoja JWT tokeno kūrimą ir dekodavimą.
    """
    user_data = {"sub": "test@viko.lt", "role": "employee"}
    token = auth_service.create_access_token(user_data)
    assert isinstance(token, str)
    decoded = auth_service.decode_access_token(token)
    assert decoded["sub"] == user_data["sub"]
    assert decoded["role"] == user_data["role"]

def test_decode_access_token_invalid():
    """
    Testuoja dekodavimą su blogu tokenu (turi mesti exception arba grąžinti None).
    """
    bad_token = "this.is.not.a.jwt"
    with pytest.raises(Exception):
        auth_service.decode_access_token(bad_token)

def test_decode_access_token_expired(monkeypatch):
    """
    Testuoja dekodavimą su pasibaigusiu JWT tokenu (jei palaikoma).
    """
    import datetime
    # Sukuria tokeną su pasibaigusia galiojimo data
    user_data = {"sub": "test@viko.lt", "role": "employee"}
    # Overwrite "expires_delta" į praeitį
    token = auth_service.create_access_token(user_data, expires_delta=datetime.timedelta(seconds=-1))
    with pytest.raises(Exception):
        auth_service.decode_access_token(token)
