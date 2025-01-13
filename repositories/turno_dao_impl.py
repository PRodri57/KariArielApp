from typing import List, Optional, Dict
from datetime import date, datetime, timedelta
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session
from models.turno import Turno
from .turno_dao import TurnoDAO
from .turno_listener import TurnoListener
from db_config import SessionLocal
import threading
import time
import asyncio
from websockets.turno_websocket import TurnoWebSocket

class TurnoDAOImpl(TurnoDAO):
    def __init__(self):
        self.db = SessionLocal()
        self.websocket = TurnoWebSocket()
        # Iniciar servidor WebSocket en un thread separado
        self.loop = asyncio.new_event_loop()
        threading.Thread(target=self._run_websocket_server, daemon=True).start()

    def _run_websocket_server(self):
        asyncio.set_event_loop(self.loop)
        import uvicorn
        uvicorn.run(self.websocket.app, host="127.0.0.1", port=8000)

    def __del__(self):
        self.detener_escucha()
        self.db.close()

    def guardar(self, turno: Turno) -> None:
        try:
            self.db.add(turno)
            self.db.commit()
            self.db.refresh(turno)
            self._notificar_cambios(turno.fecha_hora.date())
        except Exception as e:
            self.db.rollback()
            raise ValueError(f"Error al guardar turno: {str(e)}")

    def buscar_por_id(self, id: str) -> Optional[Turno]:
        return self.db.query(Turno).filter(Turno.id == id).first()

    def buscar_todos(self) -> List[Turno]:
        return self.db.query(Turno).all()

    def buscar_por_fecha(self, fecha: date, listener: Optional[TurnoListener] = None) -> List[Turno]:
        if listener:
            self._agregar_listener(fecha, listener)
            self._iniciar_polling()

        inicio_dia = datetime.combine(fecha, datetime.min.time())
        fin_dia = datetime.combine(fecha, datetime.max.time())

        return self.db.query(Turno).filter(
            and_(
                Turno.fecha_hora >= inicio_dia,
                Turno.fecha_hora <= fin_dia
            )
        ).order_by(Turno.fecha_hora).all()

    def actualizar(self, turno: Turno) -> None:
        try:
            self.db.merge(turno)
            self.db.commit()
            self._notificar_cambios(turno.fecha_hora.date())
        except Exception as e:
            self.db.rollback()
            raise ValueError(f"Error al actualizar turno: {str(e)}")

    def eliminar(self, id: str) -> None:
        try:
            turno = self.buscar_por_id(id)
            if turno:
                fecha = turno.fecha_hora.date()
                self.db.delete(turno)
                self.db.commit()
                self._notificar_cambios(fecha)
        except Exception as e:
            self.db.rollback()
            raise ValueError(f"Error al eliminar turno: {str(e)}")

    def obtener_todos(self) -> List[Turno]:
        return self.db.query(Turno).order_by(Turno.fecha_hora).all()

    def _agregar_listener(self, fecha: date, listener: TurnoListener) -> None:
        """Agrega un listener para una fecha específica"""
        if fecha not in self._listeners:
            self._listeners[fecha] = []
        self._listeners[fecha].append(listener)

    def _notificar_cambios(self, fecha: date) -> None:
        """Notifica a los listeners de una fecha específica"""
        if fecha in self._listeners:
            turnos = self.buscar_por_fecha(fecha)
            for listener in self._listeners[fecha]:
                listener.on_turnos_actualizados(turnos)

    def _iniciar_polling(self) -> None:
        """Inicia el polling de cambios si no está activo"""
        if not self._running:
            self._running = True
            self._polling_thread = threading.Thread(target=self._polling_loop)
            self._polling_thread.daemon = True
            self._polling_thread.start()

    def _polling_loop(self) -> None:
        """Loop de polling para detectar cambios"""
        while self._running:
            for fecha in list(self._listeners.keys()):
                self._notificar_cambios(fecha)
            time.sleep(5)  # Polling cada 5 segundos

    def detener_escucha(self) -> None:
        """Detiene el polling y limpia los listeners"""
        self._running = False
        if self._polling_thread:
            self._polling_thread.join(timeout=1)
        self._listeners.clear() 

    def _notificar_cambios(self, fecha: date) -> None:
        turnos = self.buscar_por_fecha(fecha)
        asyncio.run_coroutine_threadsafe(
            self.websocket.broadcast_turnos(fecha.isoformat(), turnos),
            self.loop
        ) 