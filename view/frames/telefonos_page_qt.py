from __future__ import annotations

from PySide6.QtCore import Qt
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
            # Crear contenedor para cada fila
            row_widget = QWidget()
            row_layout = QHBoxLayout(row_widget)
            row_layout.setContentsMargins(0, 0, 0, 0)
            row_layout.setSpacing(8)
            
            # Agregar celdas
            row_layout.addWidget(self._cell_label(str(tel.get("telefono_id", ""))))
            row_layout.addWidget(self._cell_label(str(tel.get("dni", ""))))
            row_layout.addWidget(self._cell_label(tel.get("marca", "")))
            row_layout.addWidget(self._cell_label(tel.get("modelo", "")))
            row_layout.addWidget(self._cell_label(tel.get("comentario", "")))
            
            # Configurar doble clic
            telefono_id = tel.get("telefono_id")
            if telefono_id:
                row_widget.mouseDoubleClickEvent = lambda event, tid=telefono_id: self._editar_telefono(tid)
                row_widget.setCursor(Qt.PointingHandCursor)
                row_widget.setStyleSheet("QWidget:hover { background: #333; }")
            
            self.grid.addWidget(row_widget, row, 0, 1, 5)  # Span 5 columnas
            row += 1

        # estirar
        self.grid.setRowStretch(row, 1)

    def _cell_label(self, text: str, extra_styles: str | None = None) -> QLabel:
        l = QLabel(text)
        styles = "QLabel { padding: 6px 4px; }"
        if extra_styles:
            styles = styles.replace("}", f" {extra_styles} }}")
        l.setStyleSheet(styles)
        l.setTextInteractionFlags(Qt.TextSelectableByMouse)
        return l

    def _editar_telefono(self, telefono_id: int) -> None:
        """Abre el diálogo de edición de teléfono"""
        dialog = EditarTelefonoDialogQt(self, telefono_id)
        if dialog.exec() == QDialog.Accepted:
            # Recargar la lista después de editar
            self._cargar_telefonos()


__all__ = ["TelefonosPage"]


