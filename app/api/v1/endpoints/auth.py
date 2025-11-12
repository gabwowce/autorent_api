# app/api/v1/endpoints/auth.py
"""
Auth endpoints: login/register/me/change-password + Google/GitHub OAuth.
"""
from datetime import date
import secrets

from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.schemas.auth import LoginRequest, TokenResponse, RegisterRequest, UserInfo, ChangePasswordRequest
from app.repositories import employee as employee_repo
from app.services.auth_service import verify_password, create_access_token, get_password_hash
from app.api.deps import get_current_user, get_db
from authlib.integrations.starlette_client import OAuth
from utils.config import settings

router = APIRouter()

# ---- Config iš settings (be hardcodų)
FRONTEND_URL = "http://localhost:3000"
GOOGLE_REDIRECT_URL = str(settings.GOOGLE_REDIRECT_URL)
GITHUB_REDIRECT_URL = str(settings.GITHUB_REDIRECT_URL) if settings.GITHUB_REDIRECT_URL else None

# ---- OAuth klientai
oauth = OAuth()

# Google – privalomas, jei naudojamas
oauth.register(
    name="google",
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

# GitHub – tik jei sukonfigūruotas
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

# ---------- GitHub ----------
@router.get("/github/login")
async def github_login(request: Request):
    if not (GITHUB_REDIRECT_URL and settings.GITHUB_CLIENT_ID and settings.GITHUB_CLIENT_SECRET):
        raise HTTPException(status_code=503, detail="GitHub OAuth neaktyvus: trūksta konfigūracijos.")
    return await oauth.github.authorize_redirect(
    request, GITHUB_REDIRECT_URL,
    allow_signup="true",          # (nebūtina)
    login="kitas_vartotojas"      # <— jei žinai login, GitHub parodys jo formą
)

@router.get("/github/callback", name="github_callback")
async def github_callback(request: Request, db: Session = Depends(get_db)):
    if not (settings.GITHUB_CLIENT_ID and settings.GITHUB_CLIENT_SECRET):
        raise HTTPException(status_code=503, detail="GitHub OAuth neaktyvus.")
    token = await oauth.github.authorize_access_token(request)
    if not token:
        raise HTTPException(status_code=400, detail="Nepavyko gauti GitHub tokeno.")

    me = (await oauth.github.get("user", token=token)).json()
    emails = (await oauth.github.get("user/emails", token=token)).json()
    email = next((e["email"] for e in emails if e.get("primary") and e.get("verified")), None) or (emails[0]["email"] if emails else None)
    if not email:
        raise HTTPException(status_code=400, detail="Nepavyko gauti el. pašto iš GitHub.")

    user = employee_repo.get_by_email(db, email)
    if not user:
        full = (me.get("name") or me.get("login") or "GitHub User").split(" ", 1)
        first, last = (full[0], (full[1] if len(full) > 1 else "User"))
        random_pwd = secrets.token_urlsafe(24)
        user = employee_repo.create_employee(db, {
            "vardas": first, "pavarde": last, "el_pastas": email,
            "telefono_nr": "", "pareigos": "Guest", "atlyginimas": 0.0,
            "isidarbinimo_data": date.today(), "slaptazodis": get_password_hash(random_pwd),
        })

    jwt_token = create_access_token(data={"sub": email, "auth": "github"})
    return RedirectResponse(url=f"http://localhost:3000/oauth#access_token={jwt_token}", status_code=303)

# ---------- Google ----------
@router.get("/google/login")
async def google_login(request: Request):
    return await oauth.google.authorize_redirect(
        request,
        GOOGLE_REDIRECT_URL,
        scope="openid email profile",
        prompt="select_account",   # <— privers rodyti paskyrų pasirinkimą
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
    if not userinfo.get("email_verified", True):
        raise HTTPException(status_code=400, detail="Google el. paštas nepatvirtintas.")

    email = userinfo["email"]
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

    jwt_token = create_access_token(data={"sub": email, "auth": "google"})
    return RedirectResponse(url=f"http://localhost:3000/oauth#access_token={jwt_token}", status_code=303)

# --------- KLASIKINIS JWT LOGIN/REGISTER ---------
@router.post("/login", response_model=TokenResponse, operation_id="login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    db_user = employee_repo.get_by_email(db, request.el_pastas)
    if not db_user or not verify_password(request.slaptazodis, db_user.slaptazodis):
        raise HTTPException(status_code=401, detail="Invalid login credentials")
    token = create_access_token(data={"sub": db_user.el_pastas})
    return TokenResponse(access_token=token)

@router.post("/register", operation_id="register")
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    if employee_repo.get_by_email(db, request.el_pastas):
        raise HTTPException(status_code=400, detail="Employee with this email already exists")
    data = request.dict()
    data["slaptazodis"] = get_password_hash(data.pop("slaptazodis"))
    new_employee = employee_repo.create_employee(db, data)
    return {"message": "Employee created successfully", "id": new_employee.darbuotojo_id}

@router.post("/logout", operation_id="logout")
def logout():
    return {"message": "Successfully logged out"}

@router.get("/me", response_model=UserInfo)
def me(current_user = Depends(get_current_user)):
    return current_user

@router.post("/change-password", operation_id="changePassword")
def change_password(request: ChangePasswordRequest, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    user = employee_repo.get_by_email(db, current_user.el_pastas)
    if not verify_password(request.senas_slaptazodis, user.slaptazodis):
        raise HTTPException(status_code=400, detail="Wrong current password")
    user.slaptazodis = get_password_hash(request.naujas_slaptazodis)
    db.commit()
    return {"message": "Password updated successfully"}

@router.post("/token", response_model=TokenResponse, operation_id="swaggerLogin")
def login_swagger(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = employee_repo.get_by_email(db, username)
    if not user or not verify_password(password, user.slaptazodis):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(data={"sub": user.el_pastas})
    return TokenResponse(access_token=token)
