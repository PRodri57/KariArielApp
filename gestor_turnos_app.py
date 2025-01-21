import sys
#import customtkinter as ctk
from config.supabase_client import supabase, get_current_user
from views.calendario_view import CalendarioView
from services.turno_service import TurnoService
from repositories.turno_repository import TurnoRepository
from views.login_view import LoginDialog

class GestorTurnosApp:
    def __init__(self):
        #ctk.set_appearance_mode("dark")  # Tema oscuro
        #ctk.set_default_color_theme("dark-blue")  # Tema de color
        
        self.app = None
        if not self.check_auth():
            sys.exit(1)
        self.setup_database()
        self.setup_services()
        self.setup_ui()

    def check_auth(self) -> bool:
        """Verifica la autenticación del usuario"""
        try:
            user = get_current_user()
            if not user:
                dialog = LoginDialog()
                dialog.mainloop()
                return dialog.result
            return True
        except Exception as e:
            print(f"Error de autenticación: {e}")
            return False

    def setup_database(self):
        """Inicializa la conexión con Supabase"""
        try:
            supabase.table('turnos').select("*").limit(1).execute()
            print("Conexión exitosa a Supabase")
        except Exception as e:
            print(f"Error al conectar a Supabase: {e}")
            sys.exit(1)

    def setup_services(self):
        """Inicializa los servicios"""
        try:
            self.turno_repository = TurnoRepository()
            self.turno_service = TurnoService(self.turno_repository)
            print("Servicios inicializados correctamente")
        except Exception as e:
            print(f"Error al inicializar servicios: {e}")
            sys.exit(1)

    def setup_ui(self):
        """Configura la interfaz de usuario"""
        try:
            self.app = CalendarioView(self.turno_service)
            self.app.mainloop()
        except Exception as e:
            print(f"Error al inicializar la interfaz: {e}")
            sys.exit(1)

def main():
    app = GestorTurnosApp()

if __name__ == "__main__":
    main()
