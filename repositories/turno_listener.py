from typing import List, Protocol
from models.turno import Turno

class TurnoListener(Protocol):
    """Protocolo para escuchar actualizaciones de turnos"""
    def on_turnos_actualizados(self, turnos: List[Turno]) -> None:
        """Llamado cuando hay actualizaciones en los turnos"""
        pass 