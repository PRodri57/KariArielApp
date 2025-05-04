# supabase.py
from supabase import create_client, Client
from dotenv import load_dotenv
import os
from utils.offline_cache import guardar_turno_local

# Cargar variables de entorno
load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Faltan las variables SUPABASE_URL o SUPABASE_KEY en el entorno")

# Crear instancia del cliente
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Funciones de autenticación
def login(email: str, password: str):
    """Inicia sesión de usuario"""
    return supabase.auth.sign_in_with_password({
        "email": email,
        "password": password
    })

def signup(email: str, password: str):
    """Registra un nuevo usuario"""
    return supabase.auth.sign_up({
        "email": email,
        "password": password
    })

def logout():
    """Cierra sesión del usuario"""
    return supabase.auth.sign_out()

def get_current_user():
    """Obtiene el usuario actual"""
    return supabase.auth.get_user()

def insertar_con_respaldo(tabla: str, datos: dict):
    try:
        respuesta = supabase.table(tabla).insert(datos).execute()
        if respuesta.error:
            raise Exception(respuesta.error)
        return respuesta
    except Exception as e:
        print(f"[CACHE] Supabase no disponible, guardando en caché: {e}")
        guardar_turno_local(tabla, datos)
        return None