from typing import Optional

from App.Schemas.cliente import ClienteCreate
from App.db.session import execute_supabase, get_supabase_client


def _cast_dni(value: Optional[object]) -> Optional[str]:
    if value is None:
        return None
    return str(value)


def listar_clientes() -> list[dict]:
    supabase = get_supabase_client()
    response = execute_supabase(
        lambda: (
            supabase.table("clientes")
            .select("*")
            .order("id", desc=True)
            .execute()
        )
    )
    rows = response.data or []
    for row in rows:
        row["dni"] = _cast_dni(row.get("dni"))
    return rows


def obtener_cliente(cliente_id: int) -> Optional[dict]:
    supabase = get_supabase_client()
    response = execute_supabase(
        lambda: (
            supabase.table("clientes")
            .select("*")
            .eq("id", cliente_id)
            .limit(1)
            .execute()
        )
    )
    rows = response.data or []
    if not rows:
        return None
    row = rows[0]
    row["dni"] = _cast_dni(row.get("dni"))
    return row


def crear_cliente(payload: ClienteCreate) -> int:
    data = {"nyape": payload.nombre, "dni": payload.dni}
    if payload.telefono_contacto:
        data["tel_contacto"] = payload.telefono_contacto
    if payload.email:
        data["email"] = payload.email
    if payload.notas:
        data["notas"] = payload.notas

    supabase = get_supabase_client()
    response = execute_supabase(
        lambda: supabase.table("clientes").insert(data).execute()
    )
    rows = response.data or []
    if not rows or "id" not in rows[0]:
        raise RuntimeError("No se pudo obtener id desde Supabase.")
    return rows[0]["id"]


def eliminar_cliente(cliente_id: int) -> bool:
    supabase = get_supabase_client()
    response = execute_supabase(
        lambda: (
            supabase.table("clientes").delete().eq("id", cliente_id).execute()
        )
    )
    return bool(response.data)
