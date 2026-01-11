from typing import Optional

from App.Schemas.telefono import TelefonoCreate, TelefonoUpdate
from App.db.session import execute_supabase, get_supabase_client


def listar_telefonos(cliente_id: Optional[int] = None) -> list[dict]:
    supabase = get_supabase_client()
    query = supabase.table("telefonos").select("*")
    if cliente_id is not None:
        query = query.eq("cliente_id", cliente_id)
    response = execute_supabase(lambda: query.order("id", desc=True).execute())
    return response.data or []


def crear_telefono(payload: TelefonoCreate) -> int:
    data = {
        "cliente_id": payload.cliente_id,
        "marca": payload.marca,
        "modelo": payload.modelo,
        "notas": payload.notas,
    }
    supabase = get_supabase_client()
    response = execute_supabase(
        lambda: supabase.table("telefonos").insert(data).execute()
    )
    rows = response.data or []
    if not rows or "id" not in rows[0]:
        raise RuntimeError("No se pudo obtener id desde Supabase.")
    return rows[0]["id"]


def actualizar_telefono(
    telefono_id: int, payload: TelefonoUpdate
) -> Optional[dict]:
    data = payload.model_dump()
    supabase = get_supabase_client()
    response = execute_supabase(
        lambda: (
            supabase.table("telefonos")
            .update(data)
            .eq("id", telefono_id)
            .execute()
        )
    )
    rows = response.data or []
    if not rows:
        return None
    return rows[0]
