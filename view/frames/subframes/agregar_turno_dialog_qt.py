from __future__ import annotations

import threading
from datetime import datetime
from typing import List, Dict, Optional

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QComboBox,
    QCalendarWidget,
    QWidget,
    QDialogButtonBox,
    QMessageBox,
)

from config.db_queries import buscar_clientes_por_dni
from model.TurnoV2 import TurnoV2
from utils.search_as_you_type_qt import SearchAsYouTypeQt


class AgregarTurnoDialogQt(QDialog):
    def __init__(self, parent: QWidget | None = None, datos_iniciales: Optional[dict] = None, on_save=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Nuevo Turno")
        self.resize(520, 520)
        self.setModal(True)

        self.datos_iniciales = datos_iniciales or {}
        self.on_save = on_save

        # Estado de búsqueda (utilidad compartida)
        self.search_helper: Optional[SearchAsYouTypeQt] = None
        self.selected_cliente: Optional[dict] = None
        self.suggestions: List[Dict] = []

        self._build_ui()

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(16, 16, 16, 16)
        root.setSpacing(10)

        # Número de orden
        root.addWidget(QLabel("Número de Orden"))
        self.entry_numero_orden = QLineEdit(self)
        self.entry_numero_orden.setPlaceholderText("Ingrese número de orden")
        self.entry_numero_orden.setText(str(self.datos_iniciales.get("numero_orden", "")))
        root.addWidget(self.entry_numero_orden)

        # DNI con autocompletado
        root.addWidget(QLabel("DNI del Cliente"))
        self.entry_dni = QLineEdit(self)
        self.entry_dni.setPlaceholderText("Ingrese DNI para buscar")
        self.entry_dni.setText(str(self.datos_iniciales.get("dni", "")))
        # Search-as-you-type helper
        self.search_helper = SearchAsYouTypeQt(
            line_edit=self.entry_dni,
            search_callable=self._buscar_cliente,
            on_results=self._on_cliente_results,
            on_started=lambda term: self.status_label.setText("Buscando cliente..."),
            on_error=lambda err, term: self._set_status_async(f"Error: {err}"),
            delay_ms=300,
            min_chars=4,
        )
        root.addWidget(self.entry_dni)

        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: #bbbbbb; font-size: 12px;")
        root.addWidget(self.status_label)

        # Teléfono
        root.addWidget(QLabel("Teléfono"))
        self.entry_telefono = QLineEdit(self)
        self.entry_telefono.setPlaceholderText("Ingrese teléfono del cliente")
        self.entry_telefono.setText(self.datos_iniciales.get("telefono", ""))
        root.addWidget(self.entry_telefono)

        # Nombre (auto)
        root.addWidget(QLabel("Nombre del Cliente"))
        self.entry_nombre = QLineEdit(self)
        self.entry_nombre.setPlaceholderText("Nombre del cliente")
        self.entry_nombre.setText(self.datos_iniciales.get("nombre", ""))
        root.addWidget(self.entry_nombre)

        # Servicio
        root.addWidget(QLabel("Servicio"))
        self.combo_servicio = QComboBox(self)
        self.combo_servicio.addItems(["Modulo", "Vidrio", "Pin de carga", "Revisión", "Otros"])
        if self.datos_iniciales.get("servicio"):
            index = self.combo_servicio.findText(self.datos_iniciales["servicio"]) or 0
            self.combo_servicio.setCurrentIndex(index)
        else:
            self.combo_servicio.setCurrentIndex(0)
        root.addWidget(self.combo_servicio)

        # Fecha de ingreso + botón calendario
        root.addWidget(QLabel("Fecha de Ingreso"))
        fecha_row = QHBoxLayout()
        self.entry_fecha = QLineEdit(self)
        self.entry_fecha.setPlaceholderText("dd/mm/yyyy o yyyy-mm-dd")
        self.entry_fecha.setText(self.datos_iniciales.get("fecha_ingreso", ""))
        fecha_row.addWidget(self.entry_fecha)
        btn_cal = QPushButton("📅", self)
        btn_cal.setFixedWidth(40)
        btn_cal.clicked.connect(self._abrir_calendario)
        fecha_row.addWidget(btn_cal)
        root.addLayout(fecha_row)

        # Presupuesto
        root.addWidget(QLabel("Presupuesto"))
        self.entry_presupuesto = QLineEdit(self)
        self.entry_presupuesto.setPlaceholderText("Ingrese presupuesto")
        self.entry_presupuesto.setText(str(self.datos_iniciales.get("presupuesto", "")))
        root.addWidget(self.entry_presupuesto)

        # Seña
        root.addWidget(QLabel("Seña"))
        self.entry_sena = QLineEdit(self)
        self.entry_sena.setPlaceholderText("Ingrese seña")
        self.entry_sena.setText(str(self.datos_iniciales.get("sena", "")))
        root.addWidget(self.entry_sena)

        # Comentario
        root.addWidget(QLabel("Comentario"))
        self.entry_comentario = QLineEdit(self)
        self.entry_comentario.setPlaceholderText("Comentario")
        self.entry_comentario.setText(self.datos_iniciales.get("comentario", ""))
        root.addWidget(self.entry_comentario)

        # Botones guardar/cancelar
        buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self._perform_save_action)
        buttons.rejected.connect(self.reject)
        root.addWidget(buttons)

        # Estilo
        self.setStyleSheet(
            """
            QDialog { background: #1f1f1f; color: #ffffff; }
            QLineEdit { background: #2b2b2b; border: 1px solid #444; border-radius: 6px; padding: 10px; color: #fff; }
            QComboBox { background: #2b2b2b; border: 1px solid #444; border-radius: 6px; padding: 6px; color: #fff; }
            QPushButton { background: #3a3a3a; border: 1px solid #444; border-radius: 6px; padding: 8px 12px; }
            QPushButton:hover { background: #454545; }
            QPushButton:pressed { background: #2f2f2f; }
            """
        )

    # ---------- AUTOCOMPLETADO DNI (utilidad compartida) ----------
    def _buscar_cliente(self, term: str) -> List[dict]:
        try:
            dni_int = int(term)
        except ValueError:
            return []
        return buscar_clientes_por_dni(dni_int) or []

    def _on_cliente_results(self, clientes: List[dict], term: str) -> None:
        # Aún no se alcanzó el mínimo: limpiar estado y salir
        if len(term) < 4:
            self.status_label.setText("")
            return
        if term != self.entry_dni.text().strip():
            return
        if not clientes:
            self.status_label.setText("No se encontraron clientes")
            return
        # Priorizar coincidencia exacta del DNI si existe
        cliente = next((c for c in clientes if str(c.get("dni")) == term), clientes[0])
        self.selected_cliente = cliente
        self.entry_nombre.setText(cliente.get("nombre_apellido", ""))
        self.status_label.setText(f"Cliente: {cliente.get('nombre_apellido', '')}")

    # ---------- CALENDARIO ----------
    def _abrir_calendario(self) -> None:
        cal = QCalendarWidget(self)
        cal.setGridVisible(True)
        cal.setWindowTitle("Seleccionar fecha")
        cal.setWindowModality(Qt.ApplicationModal)
        cal.setGeometry(self.geometry().adjusted(60, 120, -60, -120))
        cal.clicked.connect(lambda qd: self._set_fecha_from_qdate(cal, qd))
        cal.show()

    def _set_fecha_from_qdate(self, cal: QCalendarWidget, qd) -> None:
        py = datetime(qd.year(), qd.month(), qd.day())
        # Mostramos como dd/mm/yyyy pero el modelo acepta múltiples formatos
        self.entry_fecha.setText(py.strftime("%d/%m/%Y"))
        cal.close()

    # ---------- GUARDAR ----------
    def _perform_save_action(self) -> None:
        if not self._validate_form():
            return
        try:
            datos = self._collect_form_data()
            turno = TurnoV2.from_dict(datos)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Datos inválidos: {e}")
            return

        if self.on_save:
            self.on_save(turno.to_dict())
        self.accept()

    def _validate_form(self) -> bool:
        dni_str = self.entry_dni.text().strip()
        if not dni_str:
            QMessageBox.warning(self, "Campo obligatorio", "El DNI es obligatorio.")
            return False
        if not dni_str.isdigit():
            QMessageBox.warning(self, "Formato inválido", "El DNI debe ser numérico.")
            return False

        if not self.entry_nombre.text().strip():
            QMessageBox.warning(self, "Campo obligatorio", "El nombre es obligatorio.")
            return False

        if not self.entry_fecha.text().strip():
            QMessageBox.warning(self, "Campo obligatorio", "Debe seleccionar una fecha.")
            return False
        return True

    def _collect_form_data(self) -> dict:
        numero_orden_str = self.entry_numero_orden.text().strip()
        dni_str = self.entry_dni.text().strip()
        pres_str = self.entry_presupuesto.text().strip()
        sena_str = self.entry_sena.text().strip()

        numero_orden_val = int(numero_orden_str) if numero_orden_str else None
        dni_val = int(dni_str)
        pres_val = float(pres_str.replace(",", ".")) if pres_str else 0.0
        sena_val = float(sena_str.replace(",", ".")) if sena_str else 0.0

        datos = {
            "numero_orden": numero_orden_val,
            "dni": dni_val,
            "telefono_id": self.entry_telefono.text().strip(),
            "nombre": self.entry_nombre.text().strip(),
            "servicio": self.combo_servicio.currentText(),
            "fecha_ingreso": self.entry_fecha.text().strip(),
            "presupuesto": pres_val,
            "sena": sena_val,
            "comentario": self.entry_comentario.text().strip(),
        }

        if self.selected_cliente:
            datos["cliente_info"] = self.selected_cliente
        return datos

    # ---------- UTILIDADES ----------
    def _set_status_async(self, text: str) -> None:
        def set_text():
            self.status_label.setText(text)
        self._invoke_in_main(set_text)

    def _invoke_in_main(self, fn) -> None:
        QTimer.singleShot(0, fn)


__all__ = ["AgregarTurnoDialogQt"]


