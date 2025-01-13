from datetime import datetime
from dataclasses import dataclass
from typing import Optional

@dataclass
class Turno:
    id: Optional[str] = None
    nombre: str = ""
    fecha_hora: datetime = datetime.now()
    confirmado: bool = False

    def __post_init__(self):
        # Asegurarse de que fecha_hora sea datetime
        if isinstance(self.fecha_hora, str):
            self.fecha_hora = datetime.fromisoformat(self.fecha_hora)
