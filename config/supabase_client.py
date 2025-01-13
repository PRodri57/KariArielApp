from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

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