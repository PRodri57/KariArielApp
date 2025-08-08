from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QWidget,
    QDialogButtonBox,
    QMessageBox,
)

from config.db_queries import actualizar_cliente, obtener_cliente_por_dni
from model.Clientes import Cliente


class EditarClienteDialogQt(QDialog):
    def __init__(self, parent: QWidget | None = None, dni: int | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Editar Cliente")
        self.resize(500, 400)
        self.setModal(True)
        
        self.dni = dni
        self.cliente_data = None
        
        self._build_ui()
        if dni:
            self._cargar_datos()

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(16, 16, 16, 16)
        root.setSpacing(12)

        # DNI
        root.addWidget(QLabel("DNI"))
        self.entry_dni = QLineEdit(self)
        self.entry_dni.setPlaceholderText("Ingrese DNI del cliente")
        root.addWidget(self.entry_dni)

        # Nombre y Apellido
        root.addWidget(QLabel("Nombre y Apellido"))
        self.entry_nombre = QLineEdit(self)
        self.entry_nombre.setPlaceholderText("Ingrese nombre completo")
        root.addWidget(self.entry_nombre)

        # Teléfono
        root.addWidget(QLabel("Teléfono"))
        self.entry_telefono = QLineEdit(self)
        self.entry_telefono.setPlaceholderText("Ingrese teléfono")
        root.addWidget(self.entry_telefono)

        # Email
        root.addWidget(QLabel("Email"))
        self.entry_email = QLineEdit(self)
        self.entry_email.setPlaceholderText("Ingrese email (opcional)")
        root.addWidget(self.entry_email)

        # Dirección
        root.addWidget(QLabel("Dirección"))
        self.entry_direccion = QLineEdit(self)
        self.entry_direccion.setPlaceholderText("Ingrese dirección (opcional)")
        root.addWidget(self.entry_direccion)

        # Botones
        buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self._guardar)
        buttons.rejected.connect(self.reject)
        root.addWidget(buttons)

        # Estilo
        self.setStyleSheet(
            """
            QDialog { background: #1f1f1f; color: #ffffff; }
            QLineEdit { background: #2b2b2b; border: 1px solid #444; border-radius: 6px; padding: 10px; color: #fff; }
            QPushButton { background: #3a3a3a; border: 1px solid #444; border-radius: 6px; padding: 8px 12px; }
            QPushButton:hover { background: #454545; }
            QPushButton:pressed { background: #2f2f2f; }
            """
        )

    def _cargar_datos(self) -> None:
        """Carga los datos del cliente desde la base de datos"""
        if not self.dni:
            return
            
        try:
            resultado = obtener_cliente_por_dni(self.dni)
            if resultado and len(resultado) > 0:
                self.cliente_data = resultado[0]
                self._llenar_campos()
            else:
                QMessageBox.warning(self, "Error", "No se pudo cargar el cliente")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar cliente: {e}")

    def _llenar_campos(self) -> None:
        """Llena los campos con los datos del cliente"""
        if not self.cliente_data:
            return
            
        self.entry_dni.setText(str(self.cliente_data.get("dni", "")))
        self.entry_nombre.setText(self.cliente_data.get("nombre_apellido", ""))
        self.entry_telefono.setText(self.cliente_data.get("telefono", ""))
        self.entry_email.setText(self.cliente_data.get("email", ""))
        self.entry_direccion.setText(self.cliente_data.get("direccion", ""))

    def _guardar(self) -> None:
        """Guarda los cambios del cliente"""
        if not self._validar_formulario():
            return
            
        try:
            datos = {
                "dni": int(self.entry_dni.text().strip()),
                "nombre_apellido": self.entry_nombre.text().strip(),
                "telefono": self.entry_telefono.text().strip(),
                "email": self.entry_email.text().strip(),
                "direccion": self.entry_direccion.text().strip(),
            }
            
            # Crear objeto Cliente para validación
            cliente = Cliente(
                dni=datos["dni"],
                nombre_apellido=datos["nombre_apellido"],
                telefono=datos["telefono"],
                email=datos["email"],
                direccion=datos["direccion"]
            )
            
            # Guardar en base de datos
            resultado = actualizar_cliente(self.dni, datos)
            if resultado:
                QMessageBox.information(self, "Éxito", "Cliente actualizado correctamente")
                self.accept()
            else:
                QMessageBox.critical(self, "Error", "No se pudo actualizar el cliente")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al guardar: {e}")

    def _validar_formulario(self) -> bool:
        """Valida que los campos obligatorios estén completos"""
        if not self.entry_dni.text().strip():
            QMessageBox.warning(self, "Campo obligatorio", "El DNI es obligatorio.")
            return False
            
        if not self.entry_dni.text().strip().isdigit():
            QMessageBox.warning(self, "Formato inválido", "El DNI debe ser numérico.")
            return False
            
        if not self.entry_nombre.text().strip():
            QMessageBox.warning(self, "Campo obligatorio", "El nombre es obligatorio.")
            return False
            
        return True

    def get_cliente_actualizado(self) -> dict | None:
        """Retorna los datos del cliente actualizado"""
        return self.cliente_data


__all__ = ["EditarClienteDialogQt"]
