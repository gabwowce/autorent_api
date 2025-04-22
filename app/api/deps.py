from fastapi import Depends, HTTPException

from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.employee import Employee
from app.repositories.employee import get_by_email
from app.services.auth_service import SECRET_KEY, ALGORITHM
from fastapi.security import HTTPBearer
oauth2_scheme = HTTPBearer()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Employee:
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
