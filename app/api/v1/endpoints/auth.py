"""
app/api/v1/endpoints/auth.py

Authentication endpoints for employee login, registration, and profile actions.

Author: Gabrielė Tamaševičiūtė <gabriele.tamaseviciute@stud.viko.lt>

Description:
    Defines REST API endpoints for user authentication, registration, 
    password change, and profile retrieval for employees in the car rental system.
    Uses JWT for authentication and integrates with employee repository and authentication services.
"""
import os, secrets
from fastapi import APIRouter, Depends, HTTPException, Request, Form, Response
from fastapi.responses import RedirectResponse, JSONResponse
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from authlib.integrations.starlette_client import OAuth
from datetime import date
from fastapi.responses import HTMLResponse
import httpx
from app.schemas.auth import (
    LoginRequest, TokenResponse, RegisterRequest, UserInfo, ChangePasswordRequest
)
from app.api.deps import get_current_user, get_db
from app.repositories import employee as employee_repo
from app.services.auth_service import verify_password, create_access_token, get_password_hash
from utils.config import settings



load_dotenv()
router = APIRouter( tags=["Authentication"]) 


# -------- Google OAuth (OIDC) ----------

oauth = OAuth()
oauth.register(
    name="google",
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

# --- GitHub ---
if settings.GITHUB_CLIENT_ID and settings.GITHUB_CLIENT_SECRET:
    oauth.register(
        name="github",
        client_id=settings.GITHUB_CLIENT_ID,
        client_secret=settings.GITHUB_CLIENT_SECRET,
        access_token_url="https://github.com/login/oauth/access_token",
        authorize_url="https://github.com/login/oauth/authorize",
        api_base_url="https://api.github.com/",
        client_kwargs={"scope": "read:user user:email"},
    )
FRONTEND_URL = str(settings.FRONTEND_URL)
GOOGLE_REDIRECT_URL = str(settings.GOOGLE_REDIRECT_URL)
GITHUB_REDIRECT_URL = str(settings.GITHUB_REDIRECT_URL) if settings.GITHUB_REDIRECT_URL else None


@router.get("/github/login")
async def github_login(request: Request):
    if not GITHUB_REDIRECT_URL or not (settings.GITHUB_CLIENT_ID and settings.GITHUB_CLIENT_SECRET):
        raise HTTPException(status_code=503, detail="GitHub OAuth neaktyvus: trūksta konfigūracijos.")
    return await oauth.github.authorize_redirect(request, GITHUB_REDIRECT_URL)

@router.get("/github/callback", name="github_callback")
async def github_callback(request: Request, db: Session = Depends(get_db)):
    token = await oauth.github.authorize_access_token(request)
    if not token:
        raise HTTPException(status_code=400, detail="Nepavyko gauti GitHub tokeno.")

    # 1) user info
    me = (await oauth.github.get("user", token=token)).json()
    # 2) email (privatus el. paštas ateina per /user/emails)
    emails = (await oauth.github.get("user/emails", token=token)).json()
    email = next((e["email"] for e in emails if e.get("primary") and e.get("verified")), None) \
            or (emails[0]["email"] if emails else None)

    if not email:
        raise HTTPException(status_code=400, detail="Nepavyko gauti el. pašto iš GitHub.")

    # 3) sukurti / rasti user
    user = employee_repo.get_by_email(db, email)
    if not user:
        first, last = (me.get("name") or me.get("login") or "GitHub").split(" ", 1)[0], "User"
        random_pwd = secrets.token_urlsafe(24)
        user = employee_repo.create_employee(db, {
            "vardas": first, "pavarde": last, "el_pastas": email,
            "telefono_nr": "", "pareigos": "Guest", "atlyginimas": 0.0,
            "isidarbinimo_data": date.today(), "slaptazodis": get_password_hash(random_pwd),
        })

    jwt_token = create_access_token(data={"sub": email, "auth": "github", "role": user.pareigos})
    return RedirectResponse(url=f"{FRONTEND_URL}/oauth#access_token={jwt_token}", status_code=303)


@router.get("/google/login")
async def google_login(request: Request):
    return await oauth.google.authorize_redirect(
        request, GOOGLE_REDIRECT_URL, scope="openid email profile"
    )

@router.get("/google/callback", name="google_callback")
async def google_callback(request: Request, db: Session = Depends(get_db)):
    token = await oauth.google.authorize_access_token(request)

    userinfo = token.get("userinfo")
    if not userinfo:
        try:
            userinfo = await oauth.google.parse_id_token(request, token)
        except Exception:
            resp = await oauth.google.get("userinfo", token=token)
            userinfo = resp.json()

    if not userinfo or not userinfo.get("email"):
        raise HTTPException(status_code=400, detail="Nepavyko gauti Google el. pašto.")

    email = userinfo["email"]
    if not userinfo.get("email_verified", True):
        raise HTTPException(status_code=400, detail="Google el. paštas nepatvirtintas.")

    # Rasti arba sukurti darbuotoją
    user = employee_repo.get_by_email(db, email)
    if not user:
        random_pwd = secrets.token_urlsafe(24)
        employee_data = {
    "vardas": userinfo.get("given_name") or "Google",
    "pavarde": userinfo.get("family_name") or "User",   
    "el_pastas": email,
    "telefono_nr": "",
    "pareigos": "Guest",
    "atlyginimas": 0.0,
    "isidarbinimo_data": date.today(),
    "slaptazodis": get_password_hash(random_pwd),
}

        user = employee_repo.create_employee(db, employee_data)

    # Išduodam Jūsų JWT
    jwt_token = create_access_token(data={"sub": email, "auth": "google", "role": user.pareigos})

    # Variantas A: redirect į FE su token fragment’e
    return RedirectResponse(url=f"{FRONTEND_URL}/oauth#access_token={jwt_token}")


# --------- KLASIKINIS JWT LOGIN/REGISTER ---------

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
async def logout(request: Request, response: Response):
    # revoke google token (pasirinktinai)
    access_token = request.session.get("google_access_token")
    if access_token:
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                await client.post(
                    "https://oauth2.googleapis.com/revoke",
                    data={"token": access_token},
                    headers={"Content-Type": "application/x-www-form-urlencoded"},
                )
        except Exception:
            pass
    request.session.clear()
    resp = JSONResponse({"message": "Successfully logged out"})
    resp.delete_cookie("session", path="/")
    return resp


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

@router.post("/token", response_model=TokenResponse, operation_id="swaggerLogin")
def login_swagger(
    username: str = Form(...),   # čia įrašysi el. paštą
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    user = employee_repo.get_by_email(db, username)
    if not user or not verify_password(password, user.slaptazodis):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token({"sub": user.el_pastas, "role": user.pareigos})
    return TokenResponse(access_token=token, token_type="bearer")