from datetime import datetime, date, timedelta
from typing import List, Optional, Callable
from models.turno import Turno
from repositories.turno_repository import TurnoRepository

class TurnoService:
    def __init__(self, repository: TurnoRepository):
        self.repository = repository

    def agendar_turno(self, turno: Turno) -> Turno:
        """Agenda un nuevo turno verificando superposición"""
        if self.existe_superposicion(turno):
            raise ValueError("Ya existe un turno en ese horario")
        return self.repository.guardar(turno)

    def actualizar_turno(self, turno: Turno) -> Turno:
        """Actualiza un turno existente"""
        turno_original = self.repository.buscar_por_id(turno.id)
        if not turno_original:
            raise ValueError("Turno no encontrado")

        if turno.fecha_hora != turno_original.fecha_hora:
            if self.existe_superposicion(turno):
                raise ValueError("Ya existe un turno en ese horario")

        return self.repository.actualizar(turno)

    def eliminar_turno(self, turno_id: str) -> None:
        """Elimina un turno existente"""
        self.repository.eliminar(turno_id)

    def confirmar_turno(self, turno_id: str) -> Turno:
        """Confirma un turno existente"""
        turno = self.repository.buscar_por_id(turno_id)
        if not turno:
            raise ValueError("Turno no encontrado")
        
        turno.confirmado = True
        return self.repository.actualizar(turno)

    def obtener_turnos_por_fecha(self, fecha: date) -> List[Turno]:
        """Obtiene todos los turnos para una fecha específica"""
        return self.repository.buscar_por_fecha(fecha)

    def existe_superposicion(self, nuevo_turno: Turno) -> bool:
        """Verifica si hay superposición con otros turnos"""
        turnos_del_dia = self.repository.buscar_por_fecha(
            nuevo_turno.fecha_hora.date()
        )

        # Ventana de tiempo (30 minutos antes y después)
        inicio = nuevo_turno.fecha_hora - timedelta(minutes=30)
        fin = nuevo_turno.fecha_hora + timedelta(minutes=30)

        for turno in turnos_del_dia:
            if turno.id == nuevo_turno.id:
                continue

            turno_inicio = turno.fecha_hora
            turno_fin = turno.fecha_hora + timedelta(minutes=30)

            if (inicio <= turno_fin) and (fin >= turno_inicio):
                return True

        return False

    def suscribir_cambios(self, callback: Callable) -> None:
        """Suscribe a cambios en tiempo real"""
        self.repository.suscribir_cambios(callback) 