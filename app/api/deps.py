from typing import Generator
from enum import Enum

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import OAuth2PasswordBearer, HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.repositories.employee import get_by_email
from app.services.auth_service import SECRET_KEY, ALGORITHM
from app.models.employee import Employee

# Swagger password flow – turi sutapti su tavo /api/v1/token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/token")

# Alternatyvus būdas paimti gryną Bearer (naudinga jei nenaudoji OAuth2PasswordBearer)
bearer = HTTPBearer(auto_error=True)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    token: str = Depends(oauth2_scheme),        # arba: credentials: HTTPAuthorizationCredentials = Security(bearer)
    db: Session = Depends(get_db),
) -> Employee:
    """
    Iš JWT ištraukia sub (email) ir role, užkrauna vartotoją iš DB,
    normalizuoja role bei grąžina Employee su `user.role`.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    email: str | None = payload.get("sub")
    role_from_token: str | None = payload.get("role")
    if not email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token missing 'sub'")

    user = get_by_email(db, email)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Normalizuojam rolę
    effective_role = (role_from_token or getattr(user, "pareigos", "") or "Guest").strip()
    # suvienodinam registrą ir aliasus
    aliases = {
        "administratorius": "Admin",
        "admin": "Admin",
        "employee": "Emplo",
        "emplo": "Emplo",
        "user": "Guest",
        "guest": "Guest",
    }
    key = effective_role.lower()
    effective_role = aliases.get(key, effective_role.title())

    # Įrašom į runtime lauką (DB nemodifikuojam)
    setattr(user, "role", effective_role)
    return user
