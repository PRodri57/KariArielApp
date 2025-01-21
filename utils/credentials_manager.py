import json
import os
from pathlib import Path
from cryptography.fernet import Fernet

class CredentialsManager:
    def __init__(self):
        # Crear directorio de configuración si no existe
        self.config_dir = Path.home() / '.kariariel'
        self.config_dir.mkdir(exist_ok=True)
        
        # Archivo para almacenar credenciales
        self.creds_file = self.config_dir / 'credentials.json'
        
        # Archivo para la clave de encriptación
        self.key_file = self.config_dir / 'key.key'
        
        # Inicializar o cargar la clave de encriptación
        self._init_encryption_key()
        
    def _init_encryption_key(self):
        """Inicializa o carga la clave de encriptación"""
        if not self.key_file.exists():
            # Generar nueva clave si no existe
            key = Fernet.generate_key()
            with open(self.key_file, 'wb') as key_file:
                key_file.write(key)
        else:
            # Cargar clave existente
            with open(self.key_file, 'rb') as key_file:
                key = key_file.read()
        
        self.cipher_suite = Fernet(key)

    def save_credentials(self, email: str, password: str):
        """Guarda las credenciales encriptadas"""
        credentials = {
            'email': email,
            'password': password
        }
        
        # Encriptar datos
        encrypted_data = self.cipher_suite.encrypt(
            json.dumps(credentials).encode()
        )
        
        # Guardar datos encriptados
        with open(self.creds_file, 'wb') as f:
            f.write(encrypted_data)

    def load_credentials(self):
        """Carga las credenciales guardadas"""
        if not self.creds_file.exists():
            return None
            
        try:
            # Leer y desencriptar datos
            with open(self.creds_file, 'rb') as f:
                encrypted_data = f.read()
                
            decrypted_data = self.cipher_suite.decrypt(encrypted_data)
            return json.loads(decrypted_data)
        except Exception:
            # Si hay algún error, eliminar el archivo corrupto
            self.creds_file.unlink(missing_ok=True)
            return None

    def clear_credentials(self):
        """Elimina las credenciales guardadas"""
        self.creds_file.unlink(missing_ok=True) 