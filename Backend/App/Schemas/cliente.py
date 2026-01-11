from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ClienteCreate(BaseModel):
    nombre: str = Field(..., min_length=1)
    dni: str = Field(..., min_length=6, max_length=9, pattern=r"^\d+$")
    telefono_contacto: Optional[str] = None
    email: Optional[str] = None
    notas: Optional[str] = None


class ClienteCreateResponse(BaseModel):
    id: int


class ClienteOut(BaseModel):
    id: int
    dni: Optional[str] = None
    nombre: str = Field(validation_alias="nyape")
    telefono_contacto: Optional[str] = Field(
        default=None, validation_alias="tel_contacto"
    )
    email: Optional[str] = None
    notas: Optional[str] = None
    creado_en: Optional[datetime] = Field(
        default=None, validation_alias="created_at"
    )

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
