from config.supabase_client import supabase
from .offline_cache import obtener_cache, limpiar_cache

def sincronizar_cache():
    cache = obtener_cache()
    errores = False

    for tabla, filas in cache.items():
        for fila in filas:
            try:
                respuesta = supabase.table(tabla).insert(fila).execute()
                if respuesta.error:
                    print(f"[SYNC ERROR] {respuesta.error}")
                    errores = True
            except Exception as e:
                print(f"[SYNC ERROR] No se pudo insertar {fila}: {e}")
                errores = True

    if not errores:
        limpiar_cache()
        print("[SYNC] Caché sincronizada con Supabase")
    else:
        print("[SYNC] Algunos datos no se pudieron sincronizar")
