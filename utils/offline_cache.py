import json
import os
import supabase

CACHE_FILE = "turnos_cache.json"

def guardar_turno_local(turno):
    """Guarda un turno en caché local si no hay conexión"""
    turnos = []
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            turnos = json.load(f)
    turnos.append(turno)
    with open(CACHE_FILE, "w") as f:
        json.dump(turnos, f)

def obtener_turnos_locales():
    """Obtiene los turnos cacheados localmente"""
    if not os.path.exists(CACHE_FILE):
        return []
    with open(CACHE_FILE, "r") as f:
        return json.load(f)

def limpiar_cache():
    if os.path.exists(CACHE_FILE):
        os.remove(CACHE_FILE)

def sincronizar_cache():
    """Envía los turnos locales a Supabase si hay conexión"""
    turnos = obtener_turnos_locales()
    if not turnos:
        return

    for turno in turnos:
        try:
            supabase.table("turnos").insert(turno).execute()
        except Exception:
            print("Error al sincronizar un turno")
            return  # Abortamos si falla uno

    limpiar_cache()
