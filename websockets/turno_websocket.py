from fastapi import FastAPI, WebSocket
from typing import Dict, Set
import asyncio
import json
from models.turno import Turno

class TurnoWebSocket:
    def __init__(self):
        self.app = FastAPI()
        self.active_connections: Dict[str, Set[WebSocket]] = {}
        
        @self.app.websocket("/ws/{fecha}")
        async def websocket_endpoint(websocket: WebSocket, fecha: str):
            await self.connect(websocket, fecha)
            try:
                while True:
                    await websocket.receive_text()
            except:
                await self.disconnect(websocket, fecha)

    async def connect(self, websocket: WebSocket, fecha: str):
        await websocket.accept()
        if fecha not in self.active_connections:
            self.active_connections[fecha] = set()
        self.active_connections[fecha].add(websocket)

    async def disconnect(self, websocket: WebSocket, fecha: str):
        self.active_connections[fecha].remove(websocket)
        await websocket.close()

    async def broadcast_turnos(self, fecha: str, turnos: list[Turno]):
        if fecha in self.active_connections:
            turnos_json = json.dumps([{
                'id': t.id,
                'nombre': t.nombre,
                'fecha_hora': t.fecha_hora.isoformat(),
                'confirmado': t.confirmado
            } for t in turnos])
            
            for connection in self.active_connections[fecha]:
                try:
                    await connection.send_text(turnos_json)
                except:
                    await self.disconnect(connection, fecha) 