from pathlib import Path
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict

# backend/app/core/config.py -> parents[0]=core, [1]=app, [2]=backend, [3]=raíz del proyecto
_BACKEND_DIR: Path = Path(__file__).resolve().parents[2]
_ROOT_DIR: Path = _BACKEND_DIR.parent

# Precedencia: el último archivo gana (backend/.env sobrescribe al .env de la raíz).
# Las variables de entorno reales del proceso (p. ej. Render) siempre tienen prioridad.
_ENV_FILES: tuple[str, ...] = (
    str(_ROOT_DIR / ".env"),
    str(_BACKEND_DIR / ".env"),
)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=_ENV_FILES,
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    PROJECT_NAME: str = "RutaMotera API"
    API_V1_STR: str = "/api/v1"

    # Supabase
    SUPABASE_URL: str = ""
    SUPABASE_ANON_KEY: str = ""
    SUPABASE_SERVICE_ROLE_KEY: str = ""
    # Legacy: se mantiene por compatibilidad con código anterior (no requerida).
    SUPABASE_KEY: str = ""

    # OpenRouter / Agno AI
    OPENROUTER_API_KEY: str = ""
    OPENROUTER_MODEL: str = ""

    # Gemini (legacy)
    GEMINI_API_KEY: str = ""

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "https://ruta-motera.onrender.com",
    ]


settings = Settings()
