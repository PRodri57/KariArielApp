from datetime import datetime, date, timedelta
from typing import List, Optional, Callable
from models.turno import Turno
from repositories.turno_repository import TurnoRepository

class TurnoService:
    def __init__(self, turno_repository: TurnoRepository = None):
        self.turno_repository = turno_repository or TurnoRepository()

    def agendar_turno(self, turno: Turno) -> Turno:
        """Agenda un nuevo turno verificando superposición"""
        if self.existe_superposicion(turno):
            raise ValueError("Ya existe un turno en ese horario")
        return self.turno_repository.guardar(turno)

    def actualizar_turno(self, turno: Turno) -> Turno:
        """Actualiza un turno existente"""
        turno_original = self.turno_repository.buscar_por_id(turno.id)
        if not turno_original:
            raise ValueError("Turno no encontrado")

        if turno.fecha_hora != turno_original.fecha_hora:
            if self.existe_superposicion(turno):
                raise ValueError("Ya existe un turno en ese horario")

        return self.turno_repository.actualizar(turno)

    def eliminar_turno(self, turno_id: str) -> None:
        """Elimina un turno existente"""
        self.turno_repository.eliminar(turno_id)

    def confirmar_turno(self, turno_id: str) -> Turno:
        """Confirma un turno existente"""
        turno = self.turno_repository.buscar_por_id(turno_id)
        if not turno:
            raise ValueError("Turno no encontrado")
        
        turno.confirmado = True
        return self.turno_repository.actualizar(turno)

    def obtener_turnos_por_fecha(self, fecha: datetime):
        """Obtiene los turnos para una fecha específica"""
        try:
            return self.turno_repository.obtener_por_fecha(fecha)
        except Exception as e:
            print(f"Error en TurnoService.obtener_turnos_por_fecha: {str(e)}")
            raise

    def existe_superposicion(self, nuevo_turno: Turno) -> bool:
        """Verifica si hay superposición con otros turnos"""
        turnos_del_dia = self.turno_repository.buscar_por_fecha(
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
        self.turno_repository.suscribir_cambios(callback)

    def agregar_turno(self, turno: Turno):
        """Agrega un nuevo turno a la base de datos"""
        try:
            turno_dict = {
                'nombre': turno.nombre,
                'tipo_de_reparacion': turno.tipo_de_reparacion,
                'fecha_hora': turno.fecha_hora.isoformat(),
                'confirmado': turno.confirmado
            }
            
            print(f"Enviando a BD: {turno_dict}")
            
            resultado = self.turno_repository.crear(turno_dict)
            
            if resultado and 'id' in resultado:
                turno.id = resultado['id']
                return turno
            else:
                raise Exception("No se pudo crear el turno en la base de datos")
                
        except Exception as e:
            print(f"Error en TurnoService.agregar_turno: {str(e)}")
            raise

    def modificar_turno(self, turno: Turno):
        """Modifica un turno existente"""
        try:
            return self.turno_repository.actualizar(turno.id, turno)
        except Exception as e:
            print(f"Error en TurnoService.modificar_turno: {str(e)}")
            raise 