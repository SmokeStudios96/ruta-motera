"""Shim de compatibilidad. Usa app.core.database para codigo nuevo."""

from supabase import Client

from app.core.database import get_supabase_client


def get_supabase() -> Client:
    """Dependency de FastAPI (cliente anon, sujeto a RLS)."""
    return get_supabase_client()
