from __future__ import annotations

from pathlib import Path
import sys

from postgrest.exceptions import APIError

ROOT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT_DIR / "Backend"))

from App.db.errors import DatabaseUnavailableError  # noqa: E402
from App.db.session import execute_supabase, get_supabase_client  # noqa: E402


def check_connection() -> int:
    supabase = get_supabase_client()
    try:
        response = execute_supabase(
            lambda: (
                supabase.table("clientes")
                .select("id")
                .limit(1)
                .execute()
            )
        )
    except DatabaseUnavailableError as exc:
        print(f"DB no disponible: {exc.detail}")
        return 1
    except APIError as exc:
        print(f"Error Supabase: {exc}")
        return 1

    rows = response.data or []
    print(f"Conexion OK. Registros obtenidos: {len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(check_connection())
