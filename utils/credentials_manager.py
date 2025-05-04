# utils/credentials_manager.py
import json
import os
from pathlib import Path
from cryptography.fernet import Fernet

class CredentialsManager:
    def __init__(self):
        self.config_dir = Path.home() / '.kariariel'
        self.config_dir.mkdir(exist_ok=True)

        self.creds_file = self.config_dir / 'user_credentials.enc'
        self.key_file = self.config_dir / 'encryption.key'

        self._init_encryption_key()

    def _init_encryption_key(self):
        if not self.key_file.exists():
            key = Fernet.generate_key()
            with open(self.key_file, 'wb') as kf:
                kf.write(key)
        with open(self.key_file, 'rb') as kf:
            self.cipher = Fernet(kf.read())

    def save_credentials(self, email: str, password: str):
        data = {"email": email, "password": password}
        encrypted = self.cipher.encrypt(json.dumps(data).encode())
        with open(self.creds_file, 'wb') as f:
            f.write(encrypted)

    def load_credentials(self):
        if not self.creds_file.exists():
            return None
        try:
            with open(self.creds_file, 'rb') as f:
                decrypted = self.cipher.decrypt(f.read())
            return json.loads(decrypted)
        except Exception:
            self.creds_file.unlink(missing_ok=True)
            return None

    def clear_credentials(self):
        if self.creds_file.exists():
            self.creds_file.unlink()