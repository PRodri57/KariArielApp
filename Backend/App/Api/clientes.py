from fastapi import APIRouter, HTTPException, status
from postgrest.exceptions import APIError

from App.Schemas.cliente import (
    ClienteCreate,
    ClienteCreateResponse,
    ClienteOut,
)
from App.Services.clientes import (
    crear_cliente,
    listar_clientes,
    obtener_cliente,
    eliminar_cliente,
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


@router.get("", response_model=list[ClienteOut])
def listar_clientes_api() -> list[ClienteOut]:
    clientes = listar_clientes()
    return [ClienteOut.model_validate(item) for item in clientes]


@router.get("/{cliente_id}", response_model=ClienteOut)
def obtener_cliente_api(cliente_id: int) -> ClienteOut:
    cliente = obtener_cliente(cliente_id)
    if cliente is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente no encontrado.",
        )
    return ClienteOut.model_validate(cliente)


@router.post(
    "",
    response_model=ClienteCreateResponse,
    status_code=status.HTTP_201_CREATED,
)
def crear_cliente_api(payload: ClienteCreate) -> ClienteCreateResponse:
    try:
        cliente_id = crear_cliente(payload)
    except APIError as exc:
        if _pg_code(exc) == "23505":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Cliente ya existe.",
            ) from exc
        raise
    return ClienteCreateResponse(id=cliente_id)


@router.delete("/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_cliente_api(cliente_id: int) -> None:
    try:
        eliminado = eliminar_cliente(cliente_id)
    except APIError as exc:
        if _pg_code(exc) == "23503":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Cliente con telefonos asociados.",
            ) from exc
        raise
    if not eliminado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente no encontrado.",
        )
