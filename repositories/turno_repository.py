from datetime import date, datetime
from typing import List, Optional, Callable
from config.supabase_client import supabase
from models.turno import Turno

class TurnoRepository:
    def __init__(self):
        self.db = supabase

    def guardar(self, turno: Turno) -> Turno:
        """Guarda un nuevo turno"""
        try:
            result = self.db.table('turnos').insert({
                'nombre': turno.nombre,
                'fecha_hora': turno.fecha_hora.isoformat(),
                'confirmado': turno.confirmado
            }).execute()
            
            return self._map_to_turno(result.data[0])
        except Exception as e:
            raise ValueError(f"Error al guardar turno: {str(e)}")

    def actualizar(self, turno: Turno) -> Turno:
        """Actualiza un turno existente"""
        try:
            result = self.db.table('turnos')\
                .update({
                    'nombre': turno.nombre,
                    'fecha_hora': turno.fecha_hora.isoformat(),
                    'confirmado': turno.confirmado
                })\
                .eq('id', turno.id)\
                .execute()
            
            return self._map_to_turno(result.data[0])
        except Exception as e:
            raise ValueError(f"Error al actualizar turno: {str(e)}")

    def eliminar(self, turno_id: str) -> None:
        """Elimina un turno por su ID"""
        try:
            self.db.table('turnos').delete().eq('id', turno_id).execute()
        except Exception as e:
            raise ValueError(f"Error al eliminar turno: {str(e)}")

    def buscar_por_id(self, turno_id: str) -> Optional[Turno]:
        """Busca un turno por su ID"""
        try:
            result = self.db.table('turnos').select('*')\
                .eq('id', turno_id)\
                .execute()
            
            return self._map_to_turno(result.data[0]) if result.data else None
        except Exception as e:
            raise ValueError(f"Error al buscar turno: {str(e)}")

    def buscar_por_fecha(self, fecha: date) -> List[Turno]:
        """Busca todos los turnos para una fecha específica"""
        try:
            inicio = datetime.combine(fecha, datetime.min.time())
            fin = datetime.combine(fecha, datetime.max.time())
            
            result = self.db.table('turnos').select('*')\
                .gte('fecha_hora', inicio.isoformat())\
                .lte('fecha_hora', fin.isoformat())\
                .order('fecha_hora')\
                .execute()
            
            return [self._map_to_turno(data) for data in result.data]
        except Exception as e:
            raise ValueError(f"Error al buscar turnos por fecha: {str(e)}")

    def obtener_todos(self) -> List[Turno]:
        """Obtiene todos los turnos ordenados por fecha"""
        try:
            result = self.db.table('turnos').select('*')\
                .order('fecha_hora')\
                .execute()
            
            return [self._map_to_turno(data) for data in result.data]
        except Exception as e:
            raise ValueError(f"Error al obtener turnos: {str(e)}")

    def suscribir_cambios(self, callback: Callable) -> None:
        """
        Método simplificado que actualiza los datos cada vez que se llama
        en lugar de usar realtime
        """
        try:
            result = self.db.table('turnos').select('*').execute()
            turnos = [self._map_to_turno(data) for data in result.data]
            callback({'data': turnos})
        except Exception as e:
            print(f"Error al obtener cambios: {e}")

    def _map_to_turno(self, data: dict) -> Turno:
        """Convierte un diccionario de Supabase a objeto Turno"""
        return Turno(
            id=data['id'],
            nombre=data['nombre'],
            fecha_hora=datetime.fromisoformat(data['fecha_hora']),
            confirmado=data['confirmado']
        ) 