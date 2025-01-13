from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import date
from models.turno import Turno
from .turno_listener import TurnoListener

class TurnoDAO(ABC):
    """Interfaz para el acceso a datos de Turnos"""
    
    @abstractmethod
    def guardar(self, turno: Turno) -> None:
        """Guarda un nuevo turno"""
        pass

    @abstractmethod
    def buscar_por_id(self, id: str) -> Optional[Turno]:
        """Busca un turno por su ID"""
        pass

    @abstractmethod
    def buscar_todos(self) -> List[Turno]:
        """Busca todos los turnos"""
        pass

    @abstractmethod
    def buscar_por_fecha(self, fecha: date, listener: Optional[TurnoListener] = None) -> List[Turno]:
        """Busca turnos por fecha con opción de escuchar cambios"""
        pass

    @abstractmethod
    def actualizar(self, turno: Turno) -> None:
        """Actualiza un turno existente"""
        pass

    @abstractmethod
    def eliminar(self, id: str) -> None:
        """Elimina un turno por su ID"""
        pass

    @abstractmethod
    def obtener_todos(self) -> List[Turno]:
        """Obtiene todos los turnos"""
        pass
