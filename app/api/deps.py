"""
app/api/deps.py

Dependency utilities for database session management and user authentication.

Author: Gabrielė Tamaševičiūtė <gabriele.tamaseviciutes@stud.viko.lt>

Description:
    Provides reusable dependencies for:
    - Getting a database session.
    - Extracting and validating the current user from a JWT token.
"""
from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer

from app.db.session import SessionLocal
from app.models.employee import Employee
from app.repositories.employee import get_by_email
from app.services.auth_service import SECRET_KEY, ALGORITHM

oauth2_scheme = HTTPBearer()

def get_db():
    """
    Dependency to get a new SQLAlchemy database session.

    Yields:
        Session: SQLAlchemy session.

    Author: Gabrielė Tamaševičiūtė <gabriele.tamaseviciutes@stud.viko.lt>
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Employee:
    """
    Dependency to get the currently authenticated user from JWT token.

    Args:
        token (str): JWT token from Authorization header.
        db (Session): SQLAlchemy session.

    Returns:
        Employee: Authenticated user.

    Raises:
        HTTPException: If token is invalid or user not found.

    Author: Gabrielė Tamaševičiūtė <gabriele.tamaseviciutes@stud.viko.lt>
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        el_pastas: str = payload.get("sub")
        if el_pastas is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = get_by_email(db, el_pastas)
    if user is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return user
