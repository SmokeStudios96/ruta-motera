"""Fabrica de clientes Supabase para RutaMotera.

- get_supabase_admin(): usa SUPABASE_SERVICE_ROLE_KEY. Omite RLS (solo servidor).
- get_supabase_client(): usa SUPABASE_ANON_KEY. Respeta RLS.

Ambos clientes son perezosos y se cachean (singleton por proceso).
"""

import logging
from functools import lru_cache

from supabase import Client, create_client
from supabase.lib.client_options import SyncClientOptions

from app.core.config import settings

logger = logging.getLogger(__name__)

__all__ = ["get_supabase_admin", "get_supabase_client", "DatabaseConfigError"]


class DatabaseConfigError(RuntimeError):
    """Configuracion de Supabase ausente o invalida."""


def _require(name: str, value: str) -> str:
    cleaned = (value or "").strip()
    if not cleaned:
        raise DatabaseConfigError(
            f"La variable de entorno {name} no esta configurada. "
            "Definela en .env (raiz o backend/) o en el entorno del servicio."
        )
    return cleaned


def _build_client(key_name: str, key: str) -> Client:
    url = _require("SUPABASE_URL", settings.SUPABASE_URL)
    api_key = _require(key_name, key)
    options = SyncClientOptions(auto_refresh_token=False, persist_session=False)
    try:
        return create_client(url, api_key, options=options)
    except Exception as exc:
        logger.exception("No se pudo inicializar Supabase (%s)", key_name)
        raise DatabaseConfigError(f"Error creando cliente con {key_name}: {exc}") from exc


@lru_cache(maxsize=1)
def get_supabase_admin() -> Client:
    """Cliente con service role: bypass de RLS. Solo uso interno del servidor."""
    return _build_client("SUPABASE_SERVICE_ROLE_KEY", settings.SUPABASE_SERVICE_ROLE_KEY)


@lru_cache(maxsize=1)
def get_supabase_client() -> Client:
    """Cliente con anon key: sujeto a las politicas RLS."""
    return _build_client("SUPABASE_ANON_KEY", settings.SUPABASE_ANON_KEY)
