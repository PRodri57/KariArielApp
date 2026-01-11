from fastapi import APIRouter, HTTPException, Query, status
from postgrest.exceptions import APIError

from App.Schemas.telefono import (
    TelefonoCreate,
    TelefonoCreateResponse,
    TelefonoOut,
    TelefonoUpdate,
)
from App.Services.telefonos import (
    actualizar_telefono,
    crear_telefono,
    listar_telefonos,
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


@router.get("", response_model=list[TelefonoOut])
def listar_telefonos_api(
    cliente_id: int | None = Query(default=None, gt=0)
) -> list[TelefonoOut]:
    telefonos = listar_telefonos(cliente_id)
    return [TelefonoOut.model_validate(item) for item in telefonos]


@router.post(
    "",
    response_model=TelefonoCreateResponse,
    status_code=status.HTTP_201_CREATED,
)
def crear_telefono_api(payload: TelefonoCreate) -> TelefonoCreateResponse:
    try:
        telefono_id = crear_telefono(payload)
    except APIError as exc:
        if _pg_code(exc) == "23503":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente no existe.",
            ) from exc
        raise
    return TelefonoCreateResponse(id=telefono_id)


@router.put("/{telefono_id}", response_model=TelefonoOut)
def actualizar_telefono_api(
    telefono_id: int, payload: TelefonoUpdate
) -> TelefonoOut:
    telefono = actualizar_telefono(telefono_id, payload)
    if telefono is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Telefono no encontrado.",
        )
    return TelefonoOut.model_validate(telefono)
