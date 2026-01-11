from fastapi import APIRouter, HTTPException, status
from postgrest.exceptions import APIError

from App.Schemas.orden_trabajo import (
    OrdenTrabajoCreate,
    OrdenTrabajoCreateResponse,
    OrdenTrabajoOut,
    OrdenTrabajoUpdate,
)
from App.Services.ordenes_trabajo import (
    crear_orden,
    obtener_orden_por_numero,
    actualizar_orden,
    NoUpdateFieldsError,
    telefono_existe,
    telefono_tiene_orden_abierta,
)

router = APIRouter()


def _pg_code(exc: APIError) -> str | None:
    code = getattr(exc, "code", None)
    if code:
        return code
    error = getattr(exc, "error", None)
    if isinstance(error, dict):
        return error.get("code")
    return None


@router.post(
    "",
    response_model=OrdenTrabajoCreateResponse,
    status_code=status.HTTP_201_CREATED,
)
def crear_orden_trabajo(payload: OrdenTrabajoCreate) -> OrdenTrabajoCreateResponse:
    if not telefono_existe(payload.telefono_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Telefono no existe.",
        )
    if telefono_tiene_orden_abierta(payload.telefono_id):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe una orden abierta para este telefono.",
        )
    try:
        numero_orden = crear_orden(payload)
    except APIError as exc:
        if _pg_code(exc) == "23503":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Telefono no existe.",
            ) from exc
        if _pg_code(exc) == "23505":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ya existe una orden abierta para este telefono.",
            ) from exc
        raise
    return OrdenTrabajoCreateResponse(numero_orden=numero_orden)


@router.get("/{numero_orden}", response_model=OrdenTrabajoOut)
def obtener_orden_trabajo(numero_orden: int) -> OrdenTrabajoOut:
    orden = obtener_orden_por_numero(numero_orden)
    if orden is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Orden no encontrada.",
        )
    return OrdenTrabajoOut.model_validate(orden)


@router.put("/{numero_orden}", response_model=OrdenTrabajoOut)
def actualizar_orden_trabajo(
    numero_orden: int, payload: OrdenTrabajoUpdate
) -> OrdenTrabajoOut:
    try:
        orden = actualizar_orden(numero_orden, payload)
    except NoUpdateFieldsError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    if orden is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Orden no encontrada.",
        )
    return OrdenTrabajoOut.model_validate(orden)
