from typing import Optional

from App.Schemas.orden_trabajo import (
    OrdenEstado,
    OrdenTrabajoCreate,
    OrdenTrabajoUpdate,
)
from App.db.session import execute_supabase, get_supabase_client

ESTADO_TO_CODE = {
    OrdenEstado.ABIERTA: 1,
    OrdenEstado.EN_PROCESO: 2,
    OrdenEstado.ESPERANDO_REPUESTO: 3,
    OrdenEstado.LISTA: 4,
    OrdenEstado.CERRADA: 5,
    OrdenEstado.CANCELADA: 6,
}
CODE_TO_ESTADO = {value: key for key, value in ESTADO_TO_CODE.items()}


class NoUpdateFieldsError(ValueError):
    pass


def telefono_existe(telefono_id: int) -> bool:
    supabase = get_supabase_client()
    response = execute_supabase(
        lambda: (
            supabase.table("telefonos")
            .select("id")
            .eq("id", telefono_id)
            .limit(1)
            .execute()
        )
    )
    return bool(response.data)


def telefono_tiene_orden_abierta(telefono_id: int) -> bool:
    supabase = get_supabase_client()
    response = execute_supabase(
        lambda: (
            supabase.table("ordenes_de_trabajo")
            .select("id")
            .eq("tel_id", telefono_id)
            .is_("retiro", "null")
            .limit(1)
            .execute()
        )
    )
    return bool(response.data)


def crear_orden(payload: OrdenTrabajoCreate) -> int:
    supabase = get_supabase_client()
    data = {
        "tel_id": payload.telefono_id,
        "estado": ESTADO_TO_CODE[payload.estado],
        "problema": payload.problema,
        "diagnostico": payload.diagnostico,
        "presupuesto": payload.costo_estimado,
        "senia": payload.sena,
        "notas": payload.notas,
    }
    if payload.fecha_ingreso is not None:
        data["ingreso"] = payload.fecha_ingreso.isoformat()
    response = execute_supabase(
        lambda: supabase.table("ordenes_de_trabajo").insert(data).execute()
    )
    rows = response.data or []
    if not rows or "num_orden" not in rows[0]:
        raise RuntimeError("No se pudo obtener num_orden desde Supabase.")
    return rows[0]["num_orden"]


def obtener_orden_por_numero(numero_orden: int) -> Optional[dict]:
    supabase = get_supabase_client()
    response = execute_supabase(
        lambda: (
            supabase.table("ordenes_de_trabajo")
            .select("*")
            .eq("num_orden", numero_orden)
            .limit(1)
            .execute()
        )
    )
    rows = response.data or []
    if not rows:
        return None
    row = rows[0]
    estado_val = row.get("estado")
    if estado_val in CODE_TO_ESTADO:
        row["estado"] = CODE_TO_ESTADO[estado_val].value
    return row


def actualizar_orden(
    numero_orden: int, payload: OrdenTrabajoUpdate
) -> Optional[dict]:
    update_data = payload.model_dump(exclude_unset=True)
    if not update_data:
        raise NoUpdateFieldsError("No hay campos para actualizar.")
    if "estado" in update_data and update_data["estado"] is not None:
        update_data["estado"] = ESTADO_TO_CODE[update_data["estado"]]
    if "fecha_retiro" in update_data:
        fecha_retiro = update_data.pop("fecha_retiro")
        update_data["retiro"] = (
            fecha_retiro.isoformat() if fecha_retiro is not None else None
        )
    if "costo_estimado" in update_data:
        update_data["presupuesto"] = update_data.pop("costo_estimado")
    if "sena" in update_data:
        update_data["senia"] = update_data.pop("sena")
    update_data.pop("proveedor", None)
    update_data.pop("costo_final", None)
    if not update_data:
        raise NoUpdateFieldsError("No hay campos para actualizar.")

    supabase = get_supabase_client()
    response = execute_supabase(
        lambda: (
            supabase.table("ordenes_de_trabajo")
            .update(update_data)
            .eq("num_orden", numero_orden)
            .select("*")
            .limit(1)
            .execute()
        )
    )
    rows = response.data or []
    if not rows:
        return None
    row = rows[0]
    estado_val = row.get("estado")
    if estado_val in CODE_TO_ESTADO:
        row["estado"] = CODE_TO_ESTADO[estado_val].value
    return row
