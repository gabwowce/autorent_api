from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.auth import LoginRequest, TokenResponse, RegisterRequest, UserInfo
from app.db.session import SessionLocal
from app.repositories import employee as employee_repo
from app.services.auth_service import verify_password, create_access_token, get_password_hash
from app.api.deps import get_current_user, get_db

router = APIRouter()

@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    db_user = employee_repo.get_by_email(db, request.el_pastas)
    if not db_user or not verify_password(request.slaptazodis, db_user.slaptazodis):
        raise HTTPException(status_code=401, detail="Invalid login credentials")

    token = create_access_token(data={"sub": db_user.el_pastas})
    return TokenResponse(access_token=token)

@router.post("/register")
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    existing = employee_repo.get_by_email(db, request.el_pastas)
    if existing:
        raise HTTPException(status_code=400, detail="Employee with this email already exists")

    hashed = get_password_hash(request.slaptazodis)
    employee_data = request.dict()
    employee_data["slaptazodis"] = get_password_hash(employee_data.pop("slaptazodis"))


    new_employee = employee_repo.create_employee(db, employee_data)
    return {"message": "Employee created successfully", "id": new_employee.darbuotojo_id}

@router.post("/logout")
def logout():
    return {"message": "Successfully logged out"}

@router.get("/me", response_model=UserInfo)
def me(current_user = Depends(get_current_user)):
    return current_user