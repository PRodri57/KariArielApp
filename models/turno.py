from datetime import datetime
from dataclasses import dataclass
from typing import Optional

@dataclass(slots=True)
class Turno:
    nombre: str
    tipo_de_reparacion: str
    fecha_hora: datetime
    tecnico: str
    confirmado: str = "false"
    id: Optional[str] = None
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    created_by: Optional[str] = None
    

    def __post_init__(self):
        # Asegurarse de que fecha_hora sea datetime
        if isinstance(self.fecha_hora, str):
            self.fecha_hora = datetime.fromisoformat(self.fecha_hora)

    def __init__(self, nombre=None, fecha_hora=None, confirmado=False, id=None, tipo_de_reparacion=None, tecnico=None):
        self.id = id
        self.nombre = nombre
        self.fecha_hora = fecha_hora
        self.confirmado = confirmado
        self.tipo_de_reparacion = tipo_de_reparacion
        self.tecnico = tecnico

    def to_dict(self):
        return {
            "id": self.id,
            "fecha": self.fecha,
            "hora": self.hora,
            "descripcion": self.descripcion,
            "tecnico": self.tecnico
        }
