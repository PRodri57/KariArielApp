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

from config.db_queries import actualizar_telefono, obtener_telefono
from model.Telefonos import Telefono


class EditarTelefonoDialogQt(QDialog):
    def __init__(self, parent: QWidget | None = None, telefono_id: int | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Editar Teléfono")
        self.resize(500, 400)
        self.setModal(True)
        
        self.telefono_id = telefono_id
        self.telefono_data = None
        
        self._build_ui()
        if telefono_id:
            self._cargar_datos()

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(16, 16, 16, 16)
        root.setSpacing(12)

        # Teléfono ID (solo lectura)
        root.addWidget(QLabel("ID del Teléfono"))
        self.entry_telefono_id = QLineEdit(self)
        self.entry_telefono_id.setReadOnly(True)
        self.entry_telefono_id.setPlaceholderText("Se generará automáticamente")
        root.addWidget(self.entry_telefono_id)

        # DNI
        root.addWidget(QLabel("DNI del Cliente"))
        self.entry_dni = QLineEdit(self)
        self.entry_dni.setPlaceholderText("Ingrese DNI del cliente")
        root.addWidget(self.entry_dni)

        # Marca
        root.addWidget(QLabel("Marca"))
        self.entry_marca = QLineEdit(self)
        self.entry_marca.setPlaceholderText("Ej: Samsung, iPhone, etc.")
        root.addWidget(self.entry_marca)

        # Modelo
        root.addWidget(QLabel("Modelo"))
        self.entry_modelo = QLineEdit(self)
        self.entry_modelo.setPlaceholderText("Ej: Galaxy S21, iPhone 13, etc.")
        root.addWidget(self.entry_modelo)

        # Contraseña
        root.addWidget(QLabel("Contraseña"))
        self.entry_contrasena = QLineEdit(self)
        self.entry_contrasena.setPlaceholderText("Contraseña del teléfono (opcional)")
        root.addWidget(self.entry_contrasena)

        # Comentario
        root.addWidget(QLabel("Comentario"))
        self.entry_comentario = QLineEdit(self)
        self.entry_comentario.setPlaceholderText("Comentarios adicionales")
        root.addWidget(self.entry_comentario)

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
            QLineEdit:read-only { background: #333; color: #aaa; }
            QPushButton { background: #3a3a3a; border: 1px solid #444; border-radius: 6px; padding: 8px 12px; }
            QPushButton:hover { background: #454545; }
            QPushButton:pressed { background: #2f2f2f; }
            """
        )

    def _cargar_datos(self) -> None:
        """Carga los datos del teléfono desde la base de datos"""
        if not self.telefono_id:
            return
            
        try:
            resultado = obtener_telefono(self.telefono_id)
            if resultado and len(resultado) > 0:
                self.telefono_data = resultado[0]
                self._llenar_campos()
            else:
                QMessageBox.warning(self, "Error", "No se pudo cargar el teléfono")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar teléfono: {e}")

    def _llenar_campos(self) -> None:
        """Llena los campos con los datos del teléfono"""
        if not self.telefono_data:
            return
            
        self.entry_telefono_id.setText(str(self.telefono_data.get("telefono_id", "")))
        self.entry_dni.setText(str(self.telefono_data.get("dni", "")))
        self.entry_marca.setText(self.telefono_data.get("marca", ""))
        self.entry_modelo.setText(self.telefono_data.get("modelo", ""))
        self.entry_contrasena.setText(self.telefono_data.get("contrasena", ""))
        self.entry_comentario.setText(self.telefono_data.get("comentario", ""))

    def _guardar(self) -> None:
        """Guarda los cambios del teléfono"""
        if not self._validar_formulario():
            return
            
        try:
            datos = {
                "dni": int(self.entry_dni.text().strip()),
                "marca": self.entry_marca.text().strip(),
                "modelo": self.entry_modelo.text().strip(),
                "contrasena": self.entry_contrasena.text().strip(),
                "comentario": self.entry_comentario.text().strip(),
            }
            
            # Crear objeto Telefono para validación
            telefono = Telefono(
                telefono_id=self.telefono_id,
                dni=datos["dni"],
                marca=datos["marca"],
                modelo=datos["modelo"],
                contrasena=datos["contrasena"],
                comentario=datos["comentario"]
            )
            
            # Guardar en base de datos
            resultado = actualizar_telefono(self.telefono_id, datos)
            if resultado:
                QMessageBox.information(self, "Éxito", "Teléfono actualizado correctamente")
                self.accept()
            else:
                QMessageBox.critical(self, "Error", "No se pudo actualizar el teléfono")
                
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
            
        if not self.entry_marca.text().strip():
            QMessageBox.warning(self, "Campo obligatorio", "La marca es obligatoria.")
            return False
            
        if not self.entry_modelo.text().strip():
            QMessageBox.warning(self, "Campo obligatorio", "El modelo es obligatorio.")
            return False
            
        return True

    def get_telefono_actualizado(self) -> dict | None:
        """Retorna los datos del teléfono actualizado"""
        return self.telefono_data


__all__ = ["EditarTelefonoDialogQt"]
