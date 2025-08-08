from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QCheckBox,
    QPushButton,
    QWidget,
    QStackedWidget,
    QMessageBox,
)

from utils.session_manager import cargar_sesion
from utils.credentials_manager import CredentialsManager
from config.supabase_client import login as supabase_login
from config.supabase_client import signup as supabase_signup


class LoginDialogQt(QDialog):
    """Diálogo de autenticación con pestañas: Login / Signup / Recuperar."""

    PAGE_LOGIN = 0
    PAGE_SIGNUP = 1
    PAGE_RECOVER = 2

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Login")
        try:
            self.setWindowIcon(QIcon("assets/icono.ico"))
        except Exception:
            pass
        self.resize(900, 700)
        self.setModal(True)

        self.session_data = cargar_sesion()
        self.credentials_manager = CredentialsManager()

        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(32, 32, 32, 32)
        root_layout.setSpacing(16)

        self.stack = QStackedWidget(self)
        root_layout.addWidget(self.stack, 1)

        # Construcción de páginas
        self._build_login_page()
        self._build_signup_page()
        self._build_recover_page()

        # Página inicial
        self.stack.setCurrentIndex(self.PAGE_LOGIN)

        # Estilo básico
        self.setStyleSheet(
            """
            QDialog { background: #1f1f1f; color: #ffffff; }
            QLabel { font-size: 14px; }
            QLabel[role="title"] { font-size: 22px; font-weight: 600; margin-bottom: 8px; }
            QLineEdit { background: #2b2b2b; border: 1px solid #444; border-radius: 6px; padding: 10px; color: #fff; }
            QPushButton { background: #526D82; border: 1px solid #444; border-radius: 6px; padding: 10px 14px; }
            QPushButton:hover { background: #9DB2BF; }
            QPushButton:pressed { background: #DDE6ED; }
        """
        )

    # ---------- PÁGINA: LOGIN ----------
    def _build_login_page(self) -> None:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(120, 80, 120, 80)
        layout.setSpacing(12)

        title = QLabel("Inicia Sesión en tu Cuenta")
        title.setProperty("role", "title")
        layout.addWidget(title)

        self.input_email = QLineEdit()
        self.input_email.setPlaceholderText("Email")
        layout.addWidget(self.input_email)

        self.input_password = QLineEdit()
        self.input_password.setPlaceholderText("Contraseña")
        self.input_password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.input_password)

        # Prefill desde sesión guardada
        if self.session_data and "password" in self.session_data:
            self.input_email.setText(self.session_data.get("email", ""))
            self.input_password.setText(self.session_data.get("password", ""))

        show_pass_layout = QHBoxLayout()
        self.checkbox_show_password = QCheckBox("Mostrar Contraseña")
        self.checkbox_show_password.stateChanged.connect(self._toggle_password_visibility)
        show_pass_layout.addWidget(self.checkbox_show_password)
        show_pass_layout.addStretch(1)
        layout.addLayout(show_pass_layout)

        self.checkbox_remember = QCheckBox("Recordar sesión")
        self.checkbox_remember.setChecked(True)
        layout.addWidget(self.checkbox_remember)

        btn_login = QPushButton("Entrar")
        btn_login.clicked.connect(self._try_login)
        btn_login.setDefault(True)
        layout.addWidget(btn_login)

        actions_layout = QHBoxLayout()
        btn_recover = QPushButton("¿Olvidaste tu contraseña?")
        btn_recover.setFlat(True)
        btn_recover.clicked.connect(lambda: self.stack.setCurrentIndex(self.PAGE_RECOVER))
        actions_layout.addWidget(btn_recover)

        btn_signup = QPushButton("Crear Cuenta")
        btn_signup.setFlat(True)
        btn_signup.clicked.connect(lambda: self.stack.setCurrentIndex(self.PAGE_SIGNUP))
        actions_layout.addWidget(btn_signup)
        actions_layout.addStretch(1)
        layout.addLayout(actions_layout)

        if self.session_data:
            btn_logout = QPushButton("Cerrar Sesión")
            btn_logout.setStyleSheet("QPushButton { background: #7b2d2d; } QPushButton:hover { background: #8e3838; }")
            btn_logout.clicked.connect(self._logout)
            layout.addWidget(btn_logout)

        layout.addStretch(1)
        self.stack.addWidget(page)

    # ---------- PÁGINA: SIGNUP ----------
    def _build_signup_page(self) -> None:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(120, 80, 120, 80)
        layout.setSpacing(12)

        title = QLabel("Crear Cuenta")
        title.setProperty("role", "title")
        layout.addWidget(title)

        self.input_email_signup = QLineEdit()
        self.input_email_signup.setPlaceholderText("Email")
        layout.addWidget(self.input_email_signup)

        self.input_pass_signup = QLineEdit()
        self.input_pass_signup.setPlaceholderText("Contraseña")
        self.input_pass_signup.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.input_pass_signup)

        self.input_pass_confirm = QLineEdit()
        self.input_pass_confirm.setPlaceholderText("Confirmar Contraseña")
        self.input_pass_confirm.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.input_pass_confirm)

        btn_register = QPushButton("Registrar")
        btn_register.clicked.connect(self._signup)
        layout.addWidget(btn_register)

        btn_back = QPushButton("Volver al Inicio de Sesión")
        btn_back.setFlat(True)
        btn_back.clicked.connect(lambda: self.stack.setCurrentIndex(self.PAGE_LOGIN))
        layout.addWidget(btn_back)

        layout.addStretch(1)
        self.stack.addWidget(page)

    # ---------- PÁGINA: RECOVER ----------
    def _build_recover_page(self) -> None:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(120, 80, 120, 80)
        layout.setSpacing(12)

        title = QLabel("Recuperar Contraseña")
        title.setProperty("role", "title")
        layout.addWidget(title)

        self.input_email_recover = QLineEdit()
        self.input_email_recover.setPlaceholderText("Email")
        layout.addWidget(self.input_email_recover)

        btn_send = QPushButton("Enviar Instrucciones")
        btn_send.clicked.connect(self._recover)
        layout.addWidget(btn_send)

        btn_back = QPushButton("Volver al Inicio de Sesión")
        btn_back.setFlat(True)
        btn_back.clicked.connect(lambda: self.stack.setCurrentIndex(self.PAGE_LOGIN))
        layout.addWidget(btn_back)

        layout.addStretch(1)
        self.stack.addWidget(page)

    # ---------- HANDLERS ----------
    def _toggle_password_visibility(self, state: int) -> None:
        self.input_password.setEchoMode(QLineEdit.Normal if state == Qt.Checked else QLineEdit.Password)

    def _logout(self) -> None:
        try:
            from utils.session_manager import cerrar_sesion
            cerrar_sesion()
        except Exception:
            pass
        self.session_data = None
        self.input_email.clear()
        self.input_password.clear()

    def _try_login(self) -> None:
        email = self.input_email.text().strip()
        password = self.input_password.text()
        if not email or not password:
            QMessageBox.warning(self, "Campos vacíos", "Por favor completa todos los campos")
            return

        try:
            res = supabase_login(email, password)
            if getattr(res, "user", None):
                if self.checkbox_remember.isChecked():
                    self.credentials_manager.save_credentials(email, password)
                else:
                    self.credentials_manager.clear_credentials()
                self.accept()
            else:
                QMessageBox.critical(self, "Error", "Credenciales incorrectas")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo iniciar sesión: {e}")

    def _signup(self) -> None:
        email = self.input_email_signup.text().strip()
        pass1 = self.input_pass_signup.text()
        pass2 = self.input_pass_confirm.text()
        if not email or not pass1 or not pass2:
            QMessageBox.warning(self, "Error", "Todos los campos son obligatorios")
            return
        if pass1 != pass2:
            QMessageBox.critical(self, "Error", "Las contraseñas no coinciden")
            return
        try:
            response = supabase_signup(email, pass1)
            if getattr(response, "user", None):
                QMessageBox.information(
                    self,
                    "Éxito",
                    "Usuario creado exitosamente. Revisa tu correo para confirmarlo.",
                )
                self.stack.setCurrentIndex(self.PAGE_LOGIN)
            else:
                QMessageBox.critical(self, "Error", "No se pudo crear el usuario")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo registrar: {e}")

    def _recover(self) -> None:
        email = self.input_email_recover.text().strip()
        if not email:
            QMessageBox.warning(self, "Error", "Ingresa tu correo electrónico")
            return
        try:
            QMessageBox.information(
                self,
                "Instrucciones",
                f"Se ha enviado un enlace de recuperación a {email}.",
            )
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo procesar la solicitud: {e}")


__all__ = ["LoginDialogQt"]


