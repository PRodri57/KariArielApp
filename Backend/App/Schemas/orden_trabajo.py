from datetime import date, datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class OrdenEstado(str, Enum):
    ABIERTA = "ABIERTA"
    EN_PROCESO = "EN_PROCESO"
    ESPERANDO_REPUESTO = "ESPERANDO_REPUESTO"
    LISTA = "LISTA"
    CERRADA = "CERRADA"
    CANCELADA = "CANCELADA"


class OrdenTrabajoCreate(BaseModel):
    telefono_id: int = Field(..., gt=0)
    estado: OrdenEstado = OrdenEstado.ABIERTA
    fecha_ingreso: Optional[date] = None
    problema: str = Field(..., min_length=1)
    diagnostico: Optional[str] = None
    costo_estimado: Optional[int] = Field(None, ge=0)
    costo_bruto: Optional[int] = Field(None, ge=0)
    costo_revision: Optional[int] = Field(None, ge=0)
    garantia: int = Field(30, ge=0)
    proveedor: Optional[str] = None
    sena: Optional[int] = Field(None, ge=0)
    notas: Optional[str] = None


class OrdenTrabajoCreateResponse(BaseModel):
    numero_orden: int


class OrdenTrabajoOut(BaseModel):
    id: int
    numero_orden: int = Field(validation_alias="num_orden")
    telefono_id: Optional[int] = Field(default=None, validation_alias="tel_id")
    cliente_id: Optional[int] = None
    cliente_nombre: Optional[str] = None
    cliente_dni: Optional[str] = None
    cliente_telefono_contacto: Optional[str] = None
    cliente_email: Optional[str] = None
    telefono_label: Optional[str] = None
    estado: Optional[OrdenEstado] = None
    fecha_ingreso: Optional[date] = Field(default=None, validation_alias="ingreso")
    fecha_retiro: Optional[date] = Field(default=None, validation_alias="retiro")
    problema: Optional[str] = None
    diagnostico: Optional[str] = None
    costo_estimado: Optional[int] = Field(
        default=None, validation_alias="presupuesto"
    )
    costo_bruto: Optional[int] = None
    costo_revision: Optional[int] = None
    costo_final: Optional[int] = None
    garantia: Optional[int] = None
    proveedor: Optional[str] = None
    sena: Optional[int] = Field(default=None, validation_alias="sena")
    total_senas: Optional[int] = None
    resto_pagar: Optional[int] = None
    notas: Optional[str] = None

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class OrdenTrabajoUpdate(BaseModel):
    estado: Optional[OrdenEstado] = None
    fecha_retiro: Optional[date] = None
    problema: Optional[str] = Field(None, min_length=1)
    diagnostico: Optional[str] = None
    costo_estimado: Optional[int] = Field(None, ge=0)
    costo_bruto: Optional[int] = Field(None, ge=0)
    costo_revision: Optional[int] = Field(None, ge=0)
    costo_final: Optional[int] = Field(None, ge=0)
    garantia: Optional[int] = Field(None, ge=0)
    proveedor: Optional[str] = None
    sena: Optional[int] = Field(None, ge=0)
    notas: Optional[str] = None


class OrdenSenaCreate(BaseModel):
    monto: int = Field(..., gt=0)


class OrdenSenaOut(BaseModel):
    id: int
    orden_id: int
    numero_orden: int
    monto: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
