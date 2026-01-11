from typing import Callable, TypeVar

import httpx
from supabase import Client, create_client

from App.Core.config import settings
from App.db.errors import DatabaseUnavailableError

_supabase: Client = create_client(
    settings.supabase_url,
    settings.supabase_service_key,
)

T = TypeVar("T")


def get_supabase_client() -> Client:
    return _supabase


def execute_supabase(operation: Callable[[], T]) -> T:
    try:
        return operation()
    except httpx.TimeoutException as exc:
        raise DatabaseUnavailableError(
            "Timeout al conectar con Supabase."
        ) from exc
    except httpx.RequestError as exc:
        raise DatabaseUnavailableError(
            "Error de red al conectar con Supabase."
        ) from exc
