from datetime import date, datetime
from typing import List, Optional
from config.supabase_client import supabase
from models.turno import Turno

class TurnoRepository:
    def __init__(self):
        self.db = supabase

    def crear(self, turno_dict: dict):
        """Crea un nuevo turno en la base de datos"""
        try:
            result = self.db.table('turnos').insert(turno_dict).execute()
            
            if result and hasattr(result, 'data') and len(result.data) > 0:
                return result.data[0]
            else:
                raise Exception("No se recibió respuesta válida de la base de datos")
                
        except Exception as e:
            print(f"Error en TurnoRepository.crear: {str(e)}")
            raise

    def obtener_por_fecha(self, fecha: date) -> List[Turno]:
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
            print(f"Error al buscar turnos por fecha: {str(e)}")
            raise

    def actualizar(self, turno_id: str, turno: Turno) -> Turno:
        """Actualiza un turno existente"""
        try:
            turno_dict = {
                'nombre': turno.nombre,
                'tipo_de_reparacion': turno.tipo_de_reparacion,
                'fecha_hora': turno.fecha_hora.isoformat(),
                'confirmado': turno.confirmado,
                'tecnico': turno.tecnico
            }
            
            result = self.db.table('turnos')\
                .update(turno_dict)\
                .eq('id', turno_id)\
                .execute()
            
            if result and hasattr(result, 'data') and len(result.data) > 0:
                return self._map_to_turno(result.data[0])
            else:
                raise Exception("No se pudo actualizar el turno")
        except Exception as e:
            print(f"Error al actualizar turno: {str(e)}")
            raise

    def eliminar(self, turno_id: str) -> None:
        """Elimina un turno por su ID"""
        try:
            self.db.table('turnos').delete().eq('id', turno_id).execute()
        except Exception as e:
            print(f"Error al eliminar turno: {str(e)}")
            raise

    def _map_to_turno(self, data: dict) -> Turno:
        """Convierte un diccionario de la base de datos a objeto Turno"""
        return Turno(
            id=data['id'],
            nombre=data['nombre'],
            tipo_de_reparacion=data['tipo_de_reparacion'],
            fecha_hora=datetime.fromisoformat(data['fecha_hora']),
            confirmado=data['confirmado'],
            tecnico=data['tecnico']
        )