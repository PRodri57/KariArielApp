from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class TelefonoCreate(BaseModel):
    cliente_id: int = Field(..., gt=0)
    marca: str = Field(..., min_length=1)
    modelo: str = Field(..., min_length=1)
    notas: Optional[str] = None


class TelefonoCreateResponse(BaseModel):
    id: int


class TelefonoOut(BaseModel):
    id: int
    cliente_id: int
    marca: str
    modelo: str
    notas: Optional[str] = None
    creado_en: Optional[datetime] = Field(
        default=None, validation_alias="created_at"
    )

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class TelefonoUpdate(BaseModel):
    marca: str = Field(..., min_length=1)
    modelo: str = Field(..., min_length=1)
    notas: Optional[str] = None
