from pathlib import Path
from dotenv import load_dotenv            
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyHttpUrl

ENV_PATH = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=ENV_PATH, override=True, encoding="utf-8")

class Settings(BaseSettings):
    # leidžiam ignoruoti kitus .env raktus
    model_config = SettingsConfigDict(
        env_file=str(ENV_PATH),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    FRONTEND_URL: AnyHttpUrl = "http://localhost:3000"
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URL: AnyHttpUrl = "http://localhost:8000/api/v1/google/callback"

       # GitHub
    GITHUB_CLIENT_ID: str | None = None
    GITHUB_CLIENT_SECRET: str | None = None
    GITHUB_REDIRECT_URL: AnyHttpUrl | None = None

settings = Settings()

# (pasirinktinai) aiškus klaidos tekstas
for k in ("GOOGLE_CLIENT_ID", "GOOGLE_CLIENT_SECRET"):
    if not getattr(settings, k):
        raise RuntimeError(f"Trūksta env kintamojo: {k}. Patikrink {ENV_PATH}")
