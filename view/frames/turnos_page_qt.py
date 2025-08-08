from __future__ import annotations

from datetime import date, datetime

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QGridLayout,
    QScrollArea,
    QFrame,
    QDialog,
    QMessageBox,
)

from config.db_queries import obtener_turnos_por_fecha, crear_turno
from utils.offline_cache import obtener_turnos_locales
from view.components.modern_calendar_qt import ModernCalendarQt
from view.frames.subframes.agregar_turno_dialog_qt import AgregarTurnoDialogQt


class TurnosPage(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        root = QVBoxLayout(self)
        root.setContentsMargins(16, 16, 16, 16)
        root.setSpacing(12)

        # Título
        self.label_turnos = QLabel(f"Turnos del día {date.today().strftime('%d/%m/%Y')}")
        self.label_turnos.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.label_turnos.setStyleSheet("QLabel { font-size: 40px; font-weight: 700; font-family: 'Bahnschrift', sans-serif; }")
        root.addWidget(self.label_turnos)

        # Contenedor principal con grid: calendario y lista
        container = QFrame(self)
        container.setObjectName("turnosContainer")
        container.setStyleSheet("QFrame#turnosContainer { background: #252525; border: 1px solid #252525; }")
        root.addWidget(container, 1)

        grid = QGridLayout(container)
        grid.setContentsMargins(16, 16, 16, 16)
        grid.setHorizontalSpacing(16)
        grid.setVerticalSpacing(16)

        # Calendario (custom)
        self.calendar = ModernCalendarQt(container, on_select=self._on_calendar_select)
        grid.addWidget(self.calendar, 0, 0, 1, 1, Qt.AlignTop)

        # Botón nuevo turno
        self.btn_nuevo_turno = QPushButton("Nuevo Turno", container)
        self.btn_nuevo_turno.clicked.connect(self._abrir_formulario_nuevo_turno)
        self.btn_nuevo_turno.setFixedWidth(150)
        grid.addWidget(self.btn_nuevo_turno, 1, 0, 1, 1, Qt.AlignLeft | Qt.AlignTop)

        # Scroll area para la lista de turnos
        self.scroll_area = QScrollArea(container)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.NoFrame)
        grid.addWidget(self.scroll_area, 0, 1, 2, 1)

        self.list_container = QWidget()
        self.list_layout = QVBoxLayout(self.list_container)
        self.list_layout.setContentsMargins(8, 8, 8, 8)
        self.list_layout.setSpacing(10)
        self.scroll_area.setWidget(self.list_container)

        # Estado inicial
        self._cargar_turnos(self._selected_date_iso())

        # Estilos
        self.setStyleSheet(
            """
            QPushButton { background: #3a3a3a; color: #fff; border: 1px solid #444; border-radius: 6px; padding: 8px 12px; }
            QPushButton:hover { background: #454545; }
            QPushButton:pressed { background: #2f2f2f; }
            """
        )

    def _selected_date_iso(self) -> str:
        return self.calendar.get_selected_date_iso()

    def _on_calendar_select(self, dt: datetime) -> None:
        self.label_turnos.setText(f"Turnos del día {dt.strftime('%d/%m/%Y')}")
        self._cargar_turnos(dt.date().isoformat())

    def _abrir_formulario_nuevo_turno(self) -> None:
        fecha_iso = self._selected_date_iso()

        def on_save(data: dict) -> None:
            if not data.get("fecha_ingreso"):
                data["fecha_ingreso"] = fecha_iso
            try:
                res = crear_turno(data)
                if res:
                    QMessageBox.information(self, "Éxito", "Turno creado correctamente")
                else:
                    QMessageBox.critical(self, "Error", "No se pudo crear el turno")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo crear el turno: {e}")

        dialog = AgregarTurnoDialogQt(self, datos_iniciales={"fecha_ingreso": fecha_iso}, on_save=on_save)
        if dialog.exec() == QDialog.Accepted:
            self._cargar_turnos(fecha_iso)

    def _obtener_turnos_del_dia(self, fecha_iso: str) -> list[dict]:
        turnos = obtener_turnos_por_fecha(fecha_iso)
        if turnos is not None:
            return turnos
        return [t for t in obtener_turnos_locales() if t.get("fecha") == fecha_iso]

    def _cargar_turnos(self, fecha_iso: str | None = None) -> None:
        # Limpiar lista actual
        while self.list_layout.count():
            item = self.list_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        fecha_iso = fecha_iso or self._selected_date_iso()
        turnos = self._obtener_turnos_del_dia(fecha_iso)

        if not turnos:
            empty = QLabel("No hay turnos para esta fecha.")
            empty.setStyleSheet("color: #bbb; font-size: 16px;")
            self.list_layout.addWidget(empty, 0, Qt.AlignLeft | Qt.AlignTop)
            self.list_layout.addStretch(1)
            return

        for turno in turnos:
            card = self._crear_card_turno(turno)
            self.list_layout.addWidget(card)

        self.list_layout.addStretch(1)

    def _crear_card_turno(self, turno: dict) -> QWidget:
        card = QFrame()
        card.setObjectName("turnoCard")
        card.setStyleSheet(
            """
            QFrame#turnoCard { background: #333333; border: 1px solid #555555; border-radius: 10px; }
            QLabel[role="title"] { font-size: 20px; font-weight: 700; }
            QLabel[role="meta"] { color: #bbb; font-size: 12px; }
            """
        )

        v = QVBoxLayout(card)
        v.setContentsMargins(15, 12, 15, 12)
        v.setSpacing(6)

        title = QLabel(f"Orden {turno.get('numero_orden', '')} - ({turno.get('tipo_servicio', '')})")
        title.setProperty("role", "title")
        v.addWidget(title)

        detalles = []
        if turno.get("tecnico"):
            detalles.append(f"Técnico: {turno['tecnico']}")
        if detalles:
            meta = QLabel(" | ".join(detalles))
            meta.setProperty("role", "meta")
            v.addWidget(meta)

        # Interacción simple
        card.mousePressEvent = lambda e: self._seleccionar_turno(turno)
        card.enterEvent = lambda e: card.setStyleSheet(
            "QFrame#turnoCard { background: #444444; border: 1px solid #555555; border-radius: 10px; }"
        )
        card.leaveEvent = lambda e: card.setStyleSheet(
            "QFrame#turnoCard { background: #333333; border: 1px solid #555555; border-radius: 10px; }"
        )

        return card

    def _seleccionar_turno(self, turno: dict) -> None:
        msg = f"Orden: {turno.get('numero_orden', '')}\nServicio: {turno.get('tipo_servicio', '')}"
        QMessageBox.information(self, "Turno", msg)


__all__ = ["TurnosPage"]


