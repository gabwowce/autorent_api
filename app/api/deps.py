"""
app/api/deps.py

Dependency utilities for FastAPI endpoints.

Author: Gabrielė Tamaševičiūtė <gabriele.tamaseviciute@stud.viko.lt>

Description:
    Provides reusable FastAPI dependencies for database sessions and authenticated user extraction.
    Includes JWT authentication logic and DB session lifecycle management for use in API endpoints.
"""
from fastapi import Depends, HTTPException

from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.employee import Employee
from app.repositories.employee import get_by_email
from app.services.auth_service import SECRET_KEY, ALGORITHM
from fastapi.security import HTTPBearer
from fastapi.security import HTTPAuthorizationCredentials
oauth2_scheme = HTTPBearer()

def get_db():
    """
    Dependency for acquiring and releasing a database session.

    Yields:
        Session: SQLAlchemy database session.

    Author: Gabrielė Tamaševičiūtė <gabriele.tamaseviciute@stud.viko.lt>
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(
    token: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Employee:
    """
    Dependency for extracting the currently authenticated user from a JWT.

    Args:
        token (str): JWT access token from the request.
        db (Session): Database session.

    Returns:
        Employee: The authenticated employee object.

    Raises:
        HTTPException: If token is invalid or user is not found.

    Author: Gabrielė Tamaševičiūtė <gabriele.tamaseviciute@stud.viko.lt>
    """
    try:
        # Paimame tik tokeno stringą
        token_str = token.credentials  
        payload = jwt.decode(token_str, SECRET_KEY, algorithms=[ALGORITHM])
        el_pastas: str = payload.get("sub")
        if el_pastas is None:
             raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
         raise HTTPException(status_code=401, detail="Invalid token")

    user = get_by_email(db, el_pastas)
    if user is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return user
