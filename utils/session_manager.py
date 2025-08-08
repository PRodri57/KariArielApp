from utils.credentials_manager import CredentialsManager

creds_manager = CredentialsManager()

def guardar_sesion(email: str):
    """Solo guardamos el email temporalmente"""
    from mainGUI_qt import AppPrincipalQt
    AppPrincipalQt.email_guardado = email

def cargar_sesion():
    """Carga las credenciales completas desde el manager"""
    data = creds_manager.load_credentials()
    return data

def autologin():
    """Intenta hacer login automático si hay credenciales guardadas"""
    data = cargar_sesion()
    if data:
        return data["email"], data["password"]
    return None, None

def cerrar_sesion():
    """Elimina credenciales guardadas"""
    creds_manager.clear_credentials()