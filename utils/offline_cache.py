import json
import os

# Archivo donde se almacenan las operaciones pendientes. La estructura es un
# diccionario con el nombre de la tabla como clave y una lista de filas como
# valor, e.g. {"turnos": [{...}, {...}], "clientes": [{...}]}
CACHE_FILE = "cache_pendiente.json"


def guardar_turno_local(tabla: str, datos: dict) -> None:
    """Guarda una fila para la tabla dada en la caché local."""
    cache: dict[str, list] = {}
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            try:
                cache = json.load(f)
            except json.JSONDecodeError:
                cache = {}

    cache.setdefault(tabla, []).append(datos)

    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f)


def obtener_cache() -> dict:
    """Devuelve el contenido completo de la caché."""
    if not os.path.exists(CACHE_FILE):
        return {}
    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}


def obtener_turnos_locales() -> list:
    """Obtiene únicamente los turnos almacenados en la caché."""
    cache = obtener_cache()
    return cache.get("turnos", [])


def limpiar_cache() -> None:
    if os.path.exists(CACHE_FILE):
        os.remove(CACHE_FILE)


def sincronizar_cache() -> None:
    """Envía los datos cacheados a Supabase si hay conexión."""
    cache = obtener_cache()
    if not cache:
        return

    # Importación diferida para evitar dependencias circulares
    from config.supabase_client import supabase

    errores = False
    for tabla, filas in cache.items():
        for fila in filas:
            try:
                respuesta = supabase.table(tabla).insert(fila).execute()
                if getattr(respuesta, "error", None):
                    print(f"[SYNC ERROR] {respuesta.error}")
                    errores = True
            except Exception as e:  # pragma: no cover - log de sincronización
                print(f"[SYNC ERROR] No se pudo insertar {fila}: {e}")
                errores = True

    if not errores:
        limpiar_cache()
        print("[SYNC] Caché sincronizada con Supabase")
    else:
        print("[SYNC] Algunos datos no se pudieron sincronizar")
