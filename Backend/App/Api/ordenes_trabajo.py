from fastapi import APIRouter, HTTPException, Response, status
from postgrest.exceptions import APIError

from App.Schemas.orden_trabajo import (
    OrdenTrabajoCreate,
    OrdenTrabajoCreateResponse,
    OrdenTrabajoOut,
    OrdenTrabajoUpdate,
    OrdenSenaCreate,
    OrdenSenaOut,
)
from App.Services.comprobante import generar_comprobante_pdf
from App.Services.ordenes_trabajo import (
    crear_orden,
    listar_ordenes,
    obtener_orden_por_numero,
    actualizar_orden,
    listar_senas,
    agregar_sena,
    eliminar_orden,
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
        orden = crear_orden(payload)
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
    return OrdenTrabajoCreateResponse(numero_orden=orden["num_orden"])


@router.get("", response_model=list[OrdenTrabajoOut])
def listar_ordenes_trabajo() -> list[OrdenTrabajoOut]:
    ordenes = listar_ordenes()
    return [OrdenTrabajoOut.model_validate(item) for item in ordenes]


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


@router.get("/{numero_orden}/senas", response_model=list[OrdenSenaOut])
def listar_senas_orden(numero_orden: int) -> list[OrdenSenaOut]:
    senas = listar_senas(numero_orden)
    if senas is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Orden no encontrada.",
        )
    return [OrdenSenaOut.model_validate(item) for item in senas]


@router.post(
    "/{numero_orden}/senas",
    response_model=OrdenSenaOut,
    status_code=status.HTTP_201_CREATED,
)
def agregar_sena_orden(
    numero_orden: int, payload: OrdenSenaCreate
) -> OrdenSenaOut:
    sena = agregar_sena(numero_orden, payload.monto)
    if sena is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Orden no encontrada.",
        )
    return OrdenSenaOut.model_validate(sena)


@router.get("/{numero_orden}/comprobante.pdf")
def obtener_comprobante(numero_orden: int) -> Response:
    orden = obtener_orden_por_numero(numero_orden)
    if orden is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Orden no encontrada.",
        )
    senas = listar_senas(numero_orden) or []
    orden_out = OrdenTrabajoOut.model_validate(orden)
    senas_out = [OrdenSenaOut.model_validate(item) for item in senas]
    pdf_bytes = generar_comprobante_pdf(orden_out, senas_out)
    headers = {
        "Content-Disposition": f"inline; filename=comprobante-{numero_orden}.pdf"
    }
    return Response(content=pdf_bytes, media_type="application/pdf", headers=headers)


@router.delete("/{numero_orden}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_orden_trabajo(numero_orden: int) -> None:
    eliminado = eliminar_orden(numero_orden)
    if not eliminado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Orden no encontrada.",
        )
