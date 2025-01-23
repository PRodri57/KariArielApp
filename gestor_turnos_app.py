import sys
import os
import logging
from dotenv import load_dotenv
from config.supabase_client import supabase, get_current_user
from views.calendario_view import CalendarioView
from services.turno_service import TurnoService
from repositories.turno_repository import TurnoRepository
from views.login_view import LoginDialog

# Configurar logging
logging.basicConfig(
    #level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

class GestorTurnosApp:
    def __init__(self):
        logger.info("Iniciando aplicación...")
        try:
            self.load_environment()
            if not self.check_auth():
                logger.error("Fallo en la autenticación")
                sys.exit(1)
            self.setup_database()
            self.setup_services()
            self.start_app()
        except Exception as e:
            logger.exception("Error fatal en la inicialización de la app")
            sys.exit(1)

    def load_environment(self):
        """Carga las variables de entorno"""
        logger.info("Cargando variables de entorno...")
        
        # Obtener la ruta del directorio donde se encuentra el ejecutable
        if getattr(sys, 'frozen', False):
            # Si es un ejecutable, usar el directorio del ejecutable
            env_path = os.path.join(os.path.dirname(sys.executable), '.env')
        else:
            # Si es un script normal, usar el directorio del script
            env_path = os.path.join(os.path.dirname(__file__), '.env')

        if not os.path.exists(env_path):
            logger.warning("Archivo .env no encontrado, creando uno nuevo...")
            with open(env_path, 'w') as f:
                f.write("SUPABASE_URL=\n")
                f.write("SUPABASE_KEY=\n")
                f.write("SUPABASE_EMAIL=\n")
                f.write("SUPABASE_PASSWORD=\n")
            logger.error("Por favor, configura las credenciales en el archivo .env")
            sys.exit(1)
            
        load_dotenv(env_path)
        logger.info("Variables de entorno cargadas correctamente")

    def check_auth(self) -> bool:
        """Verifica la autenticación del usuario"""
        logger.info("Verificando autenticación...")
        try:
            user = get_current_user()
            if not user:
                logger.info("Usuario no autenticado, mostrando diálogo de login")
                dialog = LoginDialog()
                dialog.mainloop()
                return dialog.result
            logger.info("Usuario autenticado correctamente")
            return True
        except Exception as e:
            logger.exception("Error en la autenticación")
            return False

    def setup_database(self):
        """Inicializa la conexión con Supabase"""
        logger.info("Inicializando conexión con la base de datos...")
        try:
            supabase.table('turnos').select("*").limit(1).execute()
            logger.info("Conexión exitosa a Supabase")
        except Exception as e:
            logger.exception("Error al conectar a Supabase")
            raise

    def setup_services(self):
        """Inicializa los servicios"""
        logger.info("Inicializando servicios...")
        try:
            self.turno_repository = TurnoRepository()
            self.turno_service = TurnoService(self.turno_repository)
            logger.info("Servicios inicializados correctamente")
        except Exception as e:
            logger.exception("Error al inicializar servicios")
            raise

    def start_app(self):
        """Inicia la aplicación"""
        logger.info("Iniciando interfaz gráfica...")
        try:
            calendario = CalendarioView(self.turno_service)
            calendario.run()
            logger.info("Aplicación iniciada correctamente")
        except Exception as e:
            logger.exception("Error al iniciar la interfaz gráfica")
            raise

def main():
    try:
        logger.info("=== INICIO DE LA APLICACIÓN ===")
        app = GestorTurnosApp()
    except Exception as e:
        logger.exception("Error fatal en la aplicación")
        input("Presiona Enter para cerrar...")
        sys.exit(1)

if __name__ == "__main__":
    main()
