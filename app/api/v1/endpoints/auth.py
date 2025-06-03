"""
app/api/v1/endpoints/auth.py

API endpoints for authentication and employee account management.

Author: Gabrielė Tamaševičiūtė <gabriele.tamaseviciutes@stud.viko.lt>

Description:
    Implements RESTful API routes for authentication:
    login, register, logout, retrieve current user, and change password.
    Token-based authentication is used, with support for secure cookies.
"""
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from app.schemas.auth import LoginRequest, TokenResponse, RegisterRequest, UserInfo, ChangePasswordRequest
from app.db.session import SessionLocal
from app.repositories import employee as employee_repo
from app.services.auth_service import verify_password, create_access_token, get_password_hash
from app.api.deps import get_current_user, get_db

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/login", response_model=TokenResponse, operation_id="login")
def login(request: LoginRequest, response: Response, db: Session = Depends(get_db)):
    """
    Authenticate user and return JWT token.

    Args:
        request (LoginRequest): Login data (email and password).
        response (Response): HTTP response to set cookie.
        db (Session): SQLAlchemy session.

    Returns:
        TokenResponse: Access token if credentials are valid.

    Raises:
        HTTPException: If credentials are invalid.

    Author: Tavo Vardas <tavo.el.pastas@stud.viko.lt>
    """
    db_user = employee_repo.get_by_email(db, request.el_pastas)
    if not db_user or not verify_password(request.slaptazodis, db_user.slaptazodis):
        raise HTTPException(status_code=401, detail="Invalid login credentials")

    token = create_access_token(data={"sub": db_user.el_pastas})

    response.set_cookie(
        key="token",
        value=token,
        httponly=True,
        samesite="Lax",  
        secure=False,   
        path="/"
    )

    return {"access_token": token}

@router.post("/register", operation_id="register")
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    """
    Register a new employee.

    Args:
        request (RegisterRequest): Registration data.
        db (Session): SQLAlchemy session.

    Returns:
        dict: Success message and new employee ID.

    Raises:
        HTTPException: If email is already registered.

    Author: Tavo Vardas <tavo.el.pastas@stud.viko.lt>
    """
    existing = employee_repo.get_by_email(db, request.el_pastas)
    if existing:
        raise HTTPException(status_code=400, detail="Employee with this email already exists")

    employee_data = request.dict()
    employee_data["slaptazodis"] = get_password_hash(employee_data.pop("slaptazodis"))

    new_employee = employee_repo.create_employee(db, employee_data)
    return {"message": "Employee created successfully", "id": new_employee.darbuotojo_id}

@router.post("/logout", operation_id="logout")
def logout():
    """
    Logout current user (stateless operation).

    Returns:
        dict: Logout confirmation message.

    Author: Tavo Vardas <tavo.el.pastas@stud.viko.lt>
    """
    return {"message": "Successfully logged out"}

@router.get("/me", response_model=UserInfo)
def me(current_user = Depends(get_current_user)):
    """
    Get current logged-in user info.

    Args:
        current_user: Injected current user from token.

    Returns:
        UserInfo: Current user's information.

    Author: Tavo Vardas <tavo.el.pastas@stud.viko.lt>
    """
    return current_user

@router.post("/change-password", operation_id="changePassword")
def change_password(
    request: ChangePasswordRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Change password for current user.

    Args:
        request (ChangePasswordRequest): Current and new password.
        db (Session): SQLAlchemy session.
        current_user: Injected current user from token.

    Returns:
        dict: Password change confirmation message.

    Raises:
        HTTPException: If current password is incorrect.

    Author: Tavo Vardas <tavo.el.pastas@stud.viko.lt>
    """
    user = employee_repo.get_by_email(db, current_user.el_pastas)
    if not verify_password(request.senas_slaptazodis, user.slaptazodis):
        raise HTTPException(status_code=400, detail="Wrong current password")

    user.slaptazodis = get_password_hash(request.naujas_slaptazodis)
    db.commit()
    return {"message": "Password updated successfully"}
