"""
app/api/v1/endpoints/auth.py

Authentication endpoints for employee login, registration, and profile actions.

Author: Gabrielė Tamaševičiūtė <gabriele.tamaseviciute@stud.viko.lt>

Description:
    Defines REST API endpoints for user authentication, registration, 
    password change, and profile retrieval for employees in the car rental system.
    Uses JWT for authentication and integrates with employee repository and authentication services.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.auth import LoginRequest, TokenResponse, RegisterRequest, UserInfo, ChangePasswordRequest
from app.db.session import SessionLocal
from app.repositories import employee as employee_repo
from app.services.auth_service import verify_password, create_access_token, get_password_hash
from app.api.deps import get_current_user, get_db

router = APIRouter()

@router.post("/login", response_model=TokenResponse, operation_id="login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """
    Handle employee login. Validates credentials and returns a JWT token.

    Args:
        request (LoginRequest): Login data with email and password.
        db (Session): Database session.

    Returns:
        TokenResponse: Access token if login is successful.

    Raises:
        HTTPException: If credentials are invalid.

    Author: Gabrielė Tamaševičiūtė <gabriele.tamaseviciute@stud.viko.lt>
    """
    db_user = employee_repo.get_by_email(db, request.el_pastas)
    if not db_user or not verify_password(request.slaptazodis, db_user.slaptazodis):
        raise HTTPException(status_code=401, detail="Invalid login credentials")

    token = create_access_token(data={"sub": db_user.el_pastas})
    return TokenResponse(access_token=token)

@router.post("/register", operation_id="register")
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    """
    Register a new employee. Checks for duplicates and hashes the password.

    Args:
        request (RegisterRequest): Registration data.
        db (Session): Database session.

    Returns:
        dict: Message and created employee ID.

    Raises:
        HTTPException: If user with the same email already exists.

    Author: Gabrielė Tamaševičiūtė <gabriele.tamaseviciute@stud.viko.lt>
    """
    existing = employee_repo.get_by_email(db, request.el_pastas)
    if existing:
        raise HTTPException(status_code=400, detail="Employee with this email already exists")

    hashed = get_password_hash(request.slaptazodis)
    employee_data = request.dict()
    employee_data["slaptazodis"] = get_password_hash(employee_data.pop("slaptazodis"))


    new_employee = employee_repo.create_employee(db, employee_data)
    return {"message": "Employee created successfully", "id": new_employee.darbuotojo_id}

@router.post("/logout", operation_id="logout")
def logout():
    """
    Logout endpoint placeholder.

    Returns:
        dict: Message confirming logout.

    Author: Gabrielė Tamaševičiūtė <gabriele.tamaseviciute@stud.viko.lt>
    """
    return {"message": "Successfully logged out"}

@router.get("/me", response_model=UserInfo)
def me(current_user = Depends(get_current_user)):
    """
    Get current authenticated employee's profile.

    Args:
        current_user: Employee from authentication dependency.

    Returns:
        UserInfo: Employee profile data.

    Author: Gabrielė Tamaševičiūtė <gabriele.tamaseviciute@stud.viko.lt>
    """
    return current_user

@router.post("/change-password", operation_id="changePassword")
def change_password(
    request: ChangePasswordRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Change the current employee's password after validating the old one.

    Args:
        request (ChangePasswordRequest): Password change request data.
        db (Session): Database session.
        current_user: Authenticated employee.

    Returns:
        dict: Message confirming password change.

    Raises:
        HTTPException: If current password is incorrect.

    Author: Gabrielė Tamaševičiūtė <gabriele.tamaseviciute@stud.viko.lt>
    """
    user = employee_repo.get_by_email(db, current_user.el_pastas)
    if not verify_password(request.senas_slaptazodis, user.slaptazodis):
        raise HTTPException(status_code=400, detail="Wrong current password")

    user.slaptazodis = get_password_hash(request.naujas_slaptazodis)
    db.commit()
    return {"message": "Password updated successfully"}