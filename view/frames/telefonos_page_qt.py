from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QScrollArea,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QDialog,
)

from config.db_queries import obtener_todos_los_telefonos
from view.frames.subframes.editar_telefono_dialog_qt import EditarTelefonoDialogQt

class FilaTelefonoQt(QWidget):
    telefono_edit_requested = Signal(int)

    def __init__(self, telefono_data: dict) -> None:
        super().__init__()
        self.telefono_data = telefono_data
        self.telefono_id = telefono_data.get("telefono_id")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        layout.addWidget(self._label(str(telefono_data.get("telefono_id", ""))))
        layout.addWidget(self._label(str(telefono_data.get("dni", ""))))
        layout.addWidget(self._label(telefono_data.get("marca", "")))
        layout.addWidget(self._label(telefono_data.get("modelo", "")))
        layout.addWidget(self._label(telefono_data.get("comentario", "")))

        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet("QWidget:hover { background: #333; }")

    def _label(self, text: str) -> QLabel:
        l = QLabel(text)
        l.setAttribute(Qt.WA_TransparentForMouseEvents)
        l.setStyleSheet("QLabel { padding: 6px 4px; }")
        return l

    def mouseDoubleClickEvent(self, event) -> None:
        print("DEBUG: Ingreso a mouseDoubleClickEvent")
        if self.telefono_id is not None:
            print("DEBUG: Cumplio condicion y termino de entrar")
            self.telefono_edit_requested.emit(self.telefono_id)
        super().mouseDoubleClickEvent(event)

class TelefonosPage(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        root = QVBoxLayout(self)
        root.setContentsMargins(16, 16, 16, 16)
        root.setSpacing(12)

        title = QLabel("Teléfonos")
        title.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        title.setStyleSheet("QLabel { font-size: 40px; font-weight: 700; font-family: 'Bahnschrift', sans-serif; }")
        root.addWidget(title)

        container = QFrame(self)
        container.setObjectName("telefonosContainer")
        container.setStyleSheet("QFrame#telefonosContainer { background: #252525; border: 1px solid #252525; }")
        root.addWidget(container, 1)

        layout = QVBoxLayout(container)
        layout.setContentsMargins(16, 16, 16, 16)

        scroll = QScrollArea(container)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        layout.addWidget(scroll)

        self.content = QWidget()
        self.grid = QGridLayout(self.content)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setHorizontalSpacing(8)
        self.grid.setVerticalSpacing(8)
        scroll.setWidget(self.content)

        self._cargar_telefonos()

    def _cargar_telefonos(self) -> None:
        # Limpiar
        while self.grid.count():
            item = self.grid.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()

        telefonos = obtener_todos_los_telefonos() or []

        if not telefonos:
            empty = QLabel("No hay teléfonos registrados.")
            empty.setStyleSheet("color: #bbb; font-size: 16px;")
            self.grid.addWidget(empty, 0, 0, Qt.AlignLeft | Qt.AlignTop)
            return

        # Encabezados
        header_styles = "color: #ddd; font-weight: 600; border-bottom: 1px solid #444; padding: 6px 4px;"
        self.grid.addWidget(self._cell_label("Teléfono ID", header_styles), 0, 0)
        self.grid.addWidget(self._cell_label("DNI", header_styles), 0, 1)
        self.grid.addWidget(self._cell_label("Marca", header_styles), 0, 2)
        self.grid.addWidget(self._cell_label("Modelo", header_styles), 0, 3)
        self.grid.addWidget(self._cell_label("Comentario", header_styles), 0, 4)

        row = 1
        for tel in telefonos:
            #print("DEBUG: Ingreso al for")
            fila = FilaTelefonoQt(tel)
            fila.telefono_edit_requested.connect(self._editar_telefono)
            #print("DEBUG: Conecto telefono_edit_requested")
            self.grid.addWidget(fila, row, 0, 1, 5)
            row += 1

        # estirar
        self.grid.setRowStretch(row, 1)

    def _cell_label(self, text: str, extra_styles: str | None = None) -> QLabel:
        l = QLabel(text)
        styles = "QLabel { padding: 6px 4px; }"
        if extra_styles:
            styles = styles.replace("}", f" {extra_styles} }}")
        l.setStyleSheet(styles)
        #l.setAttribute(Qt.WA_TransparentForMouseEvents)
        return l

    def _editar_telefono(self, telefono_id: int) -> None:
        """Abre el diálogo de edición de teléfono"""
        print("DEBUG: Ingreso a _editar_telefono")
        dialog = EditarTelefonoDialogQt(self, telefono_id)
        if dialog.exec() == QDialog.Accepted:
            self._cargar_telefonos()


__all__ = ["TelefonosPage"]


