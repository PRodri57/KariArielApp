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


def _normalizar_estado(row: dict) -> None:
    estado_val = row.get("estado")
    if estado_val in CODE_TO_ESTADO:
        row["estado"] = CODE_TO_ESTADO[estado_val].value


def _normalizar_sena(row: dict) -> None:
    if row.get("sena") is None and row.get("senia") is not None:
        row["sena"] = row["senia"]


def _agregar_totales(row: dict) -> None:
    total_senas = row.get("sena") or row.get("senia") or 0
    row["total_senas"] = total_senas
    presupuesto = row.get("presupuesto")
    if presupuesto is None:
        row["resto_pagar"] = None
    else:
        row["resto_pagar"] = presupuesto - total_senas


def _enriquecer_relaciones(row: dict) -> None:
    telefono = row.pop("telefonos", None)
    if isinstance(telefono, list):
        telefono = telefono[0] if telefono else None
    if not isinstance(telefono, dict):
        return
    marca = telefono.get("marca")
    modelo = telefono.get("modelo")
    if marca or modelo:
        row["telefono_label"] = " ".join(
            item for item in [marca, modelo] if item
        )
    cliente_id = telefono.get("cliente_id")
    if cliente_id is not None:
        row["cliente_id"] = cliente_id
    cliente = telefono.get("clientes")
    if isinstance(cliente, list):
        cliente = cliente[0] if cliente else None
    if isinstance(cliente, dict):
        nombre = cliente.get("nyape")
        if nombre:
            row["cliente_nombre"] = nombre


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


def crear_orden(payload: OrdenTrabajoCreate) -> dict:
    supabase = get_supabase_client()
    data = {
        "tel_id": payload.telefono_id,
        "estado": ESTADO_TO_CODE[payload.estado],
        "problema": payload.problema,
        "diagnostico": payload.diagnostico,
        "presupuesto": payload.costo_estimado,
        "costo_bruto": payload.costo_bruto,
        "costo_revision": payload.costo_revision,
        "proveedor": payload.proveedor,
        "sena": payload.sena,
        "sena_revision": payload.sena_revision,
        "notas": payload.notas,
    }
    if payload.fecha_ingreso is not None:
        data["ingreso"] = payload.fecha_ingreso.isoformat()
    response = execute_supabase(
        lambda: supabase.table("ordenes_de_trabajo").insert(data).execute()
    )
    rows = response.data or []
    if not rows or "num_orden" not in rows[0] or "id" not in rows[0]:
        raise RuntimeError("No se pudo obtener num_orden desde Supabase.")
    row = rows[0]
    if payload.sena:
        execute_supabase(
            lambda: (
                supabase.table("ordenes_senas")
                .insert({"orden_id": row["id"], "monto": payload.sena})
                .execute()
            )
        )
    return row


def listar_ordenes() -> list[dict]:
    supabase = get_supabase_client()
    response = execute_supabase(
        lambda: (
            supabase.table("ordenes_de_trabajo")
            .select(
                "*, telefonos (id, marca, modelo, cliente_id, clientes (id, nyape))"
            )
            .order("num_orden", desc=True)
            .execute()
        )
    )
    rows = response.data or []
    for row in rows:
        _normalizar_estado(row)
        _normalizar_sena(row)
        _agregar_totales(row)
        _enriquecer_relaciones(row)
    return rows


def obtener_orden_por_numero(numero_orden: int) -> Optional[dict]:
    supabase = get_supabase_client()
    response = execute_supabase(
        lambda: (
            supabase.table("ordenes_de_trabajo")
            .select(
                "*, telefonos (id, marca, modelo, cliente_id, clientes (id, nyape))"
            )
            .eq("num_orden", numero_orden)
            .limit(1)
            .execute()
        )
    )
    rows = response.data or []
    if not rows:
        return None
    row = rows[0]
    _normalizar_estado(row)
    _normalizar_sena(row)
    _agregar_totales(row)
    _enriquecer_relaciones(row)
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
    update_data.pop("costo_final", None)
    if not update_data:
        raise NoUpdateFieldsError("No hay campos para actualizar.")

    supabase = get_supabase_client()
    response = execute_supabase(
        lambda: (
            supabase.table("ordenes_de_trabajo")
            .update(update_data)
            .eq("num_orden", numero_orden)
            .execute()
        )
    )
    rows = response.data or []
    if not rows:
        return None
    row = rows[0]
    _normalizar_estado(row)
    _normalizar_sena(row)
    _agregar_totales(row)
    return row


def _obtener_orden_basica(numero_orden: int) -> Optional[dict]:
    supabase = get_supabase_client()
    response = execute_supabase(
        lambda: (
            supabase.table("ordenes_de_trabajo")
            .select("id, num_orden, presupuesto, sena, senia")
            .eq("num_orden", numero_orden)
            .limit(1)
            .execute()
        )
    )
    rows = response.data or []
    if not rows:
        return None
    row = rows[0]
    _normalizar_sena(row)
    _agregar_totales(row)
    return row


def listar_senas(numero_orden: int) -> Optional[list[dict]]:
    orden = _obtener_orden_basica(numero_orden)
    if orden is None:
        return None
    supabase = get_supabase_client()
    response = execute_supabase(
        lambda: (
            supabase.table("ordenes_senas")
            .select("id, orden_id, monto, created_at")
            .eq("orden_id", orden["id"])
            .order("created_at", desc=True)
            .execute()
        )
    )
    rows = response.data or []
    for row in rows:
        row["numero_orden"] = numero_orden
    return rows


def agregar_sena(numero_orden: int, monto: int) -> Optional[dict]:
    orden = _obtener_orden_basica(numero_orden)
    if orden is None:
        return None
    supabase = get_supabase_client()
    response = execute_supabase(
        lambda: (
            supabase.table("ordenes_senas")
            .insert({"orden_id": orden["id"], "monto": monto})
            .execute()
        )
    )
    rows = response.data or []
    if not rows:
        return None
    total_actual = (orden.get("sena") or 0) + monto
    execute_supabase(
        lambda: (
            supabase.table("ordenes_de_trabajo")
            .update({"sena": total_actual})
            .eq("id", orden["id"])
            .execute()
        )
    )
    row = rows[0]
    row["numero_orden"] = numero_orden
    return row


def eliminar_orden(numero_orden: int) -> bool:
    supabase = get_supabase_client()
    response = execute_supabase(
        lambda: (
            supabase.table("ordenes_de_trabajo")
            .select("id")
            .eq("num_orden", numero_orden)
            .limit(1)
            .execute()
        )
    )
    rows = response.data or []
    if not rows:
        return False
    orden_id = rows[0]["id"]
    execute_supabase(
        lambda: (
            supabase.table("ordenes_senas")
            .delete()
            .eq("orden_id", orden_id)
            .execute()
        )
    )
    response = execute_supabase(
        lambda: (
            supabase.table("ordenes_de_trabajo")
            .delete()
            .eq("id", orden_id)
            .execute()
        )
    )
    return bool(response.data)
