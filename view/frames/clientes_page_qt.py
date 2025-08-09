from __future__ import annotations

import threading
from typing import Optional, List

from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QScrollArea,
    QFrame,
    QHBoxLayout,
    QDialog
)

from config.db_queries import obtener_todos_los_clientes, buscar_clientes_por_dni
from view.frames.subframes.editar_cliente_dialog_qt import EditarClienteDialogQt
from model.Clientes import Cliente
from utils.search_as_you_type_qt import SearchAsYouTypeQt


class TarjetaClienteQt(QFrame):
    cliente_edit_requested = Signal(int)
    def __init__(self, parent: QWidget | None, cliente_data: dict) -> None:
        super().__init__(parent)
        self.setObjectName("TarjetaCliente")
        self.setStyleSheet(
            """
            QFrame#TarjetaCliente { background: #2c2c2c; border: 1px solid #3a3a3a; border-radius: 10px; }
            QLabel[role="name"] { font-size: 18px; font-weight: 700; }
            QLabel[role="meta"] { color: #bbbbbb; }
            """
        )

        cliente = Cliente.from_dict(cliente_data)

        root = QVBoxLayout(self)
        root.setContentsMargins(15, 12, 15, 12)
        root.setSpacing(6)

        nombre = QLabel(cliente.nombre_apellido)
        nombre.setProperty("role", "name")
        root.addWidget(nombre)

        dni = QLabel(f"DNI: {cliente.dni}")
        dni.setProperty("role", "meta")
        root.addWidget(dni)

        if cliente.telefono:
            telefono = QLabel(f"Teléfono: {cliente.telefono}")
            telefono.setProperty("role", "meta")
            root.addWidget(telefono)

        if cliente.email:
            email = QLabel(f"Email: {cliente.email}")
            email.setProperty("role", "meta")
            root.addWidget(email)

        if cliente.direccion:
            direccion = QLabel(f"Dirección: {cliente.direccion}")
            direccion.setProperty("role", "meta")
            root.addWidget(direccion)

        # Configurar doble clic
        self.cliente_data = cliente_data
        self.mouseDoubleClickEvent = self._on_double_click
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet(
            """
            QFrame#TarjetaCliente { background: #2c2c2c; border: 1px solid #3a3a3a; border-radius: 10px; }
            QFrame#TarjetaCliente:hover { background: #3a3a3a; border: 1px solid #4a4a4a; }
            QLabel[role="name"] { font-size: 18px; font-weight: 700; }
            QLabel[role="meta"] { color: #bbbbbb; }
            """
        )

    def _on_double_click(self, event) -> None:
        """Maneja el evento de doble click en la tarjeta"""
        #print("DEBUG: Ingreso a mouseDoubleClickEvent")
        dni = self.cliente_data.get("dni")
        if dni:
            self.cliente_edit_requested.emit(dni)


class ClientesPage(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.debouncer: Optional[SearchAsYouTypeQt] = None

        root = QVBoxLayout(self)
        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(12)

        # Título
        titulo = QLabel("Lista de Clientes")
        titulo.setStyleSheet("QLabel { font-size: 40px; font-weight: 700; font-family: 'Bahnschrift', sans-serif; }")
        root.addWidget(titulo)

        # Buscador
        buscador_container = QVBoxLayout()

        buscador_label = QLabel("Buscar por DNI:")
        buscador_label.setStyleSheet("QLabel { font-size: 16px; font-weight: 700; }")
        buscador_container.addWidget(buscador_label)

        self.search_entry = QLineEdit()
        self.search_entry.setPlaceholderText("Ingresa el DNI del cliente...")
        self.search_entry.setFixedHeight(40)
        # Search-as-you-type helper
        self.debouncer = SearchAsYouTypeQt(
            line_edit=self.search_entry,
            search_callable=self._buscar_clientes,
            on_results=self._on_search_results,
            on_started=lambda term: self.status_label.setText("Buscando..." if len(term) >= 1 else ""),
            on_error=lambda err, term: self._set_status_async(f"Error en la búsqueda: {err}"),
            delay_ms=500,
            min_chars=1,
        )
        buscador_container.addWidget(self.search_entry)

        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: #bbbbbb; font-size: 12px;")
        buscador_container.addWidget(self.status_label)

        root.addLayout(buscador_container)

        # Scroll de resultados
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.NoFrame)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        root.addWidget(self.scroll_area, 1)

        self.results_container = QWidget()
        self.results_layout = QVBoxLayout(self.results_container)
        self.results_layout.setContentsMargins(8, 8, 8, 8)
        self.results_layout.setSpacing(8)
        self.results_layout.setAlignment(Qt.AlignTop)
        self.scroll_area.setWidget(self.results_container)

        # Estilos globales básicos
        self.setStyleSheet(
            """
            QLineEdit { background: #2b2b2b; border: 1px solid #444; border-radius: 6px; padding: 10px; color: #fff; }
            """
        )

        # Cargar clientes iniciales
        self.cargar_clientes()

    # ---------- BÚSQUEDA (utilitario compartido) ----------
    def _buscar_clientes(self, term: str) -> List[dict]:
        print(f"DEBUG: Buscando clientes con término: '{term}'")
        if len(term) == 0:
            print("DEBUG: Término vacío, retornando lista vacía")
            return []
        try:
            dni_int = int(term)
            print(f"DEBUG: DNI convertido a int: {dni_int}")
        except ValueError:
            print(f"DEBUG: Error convirtiendo '{term}' a int")
            return []
        
        resultados = buscar_clientes_por_dni(dni_int) or []
        print(f"DEBUG: Resultados de búsqueda: {len(resultados)} clientes")
        return resultados

    def _on_search_results(self, clientes_data: List[dict], search_term: str) -> None:
        print(f"DEBUG: _on_search_results llamado con {len(clientes_data)} clientes, término: '{search_term}'")
        if len(search_term) == 0:
            print("DEBUG: Término vacío, cargando todos los clientes")
            self.status_label.setText("")
            self.cargar_clientes()
            return
        print("DEBUG: Mostrando resultados de búsqueda")
        self._display_search_results_async(clientes_data, search_term)

    # ---------- CARGA INICIAL ----------
    def cargar_clientes(self) -> None:
        # Cargar directamente en el hilo principal para evitar problemas de sincronización
        self._cargar_clientes_sync()

    def _cargar_clientes_sync(self) -> None:
        try:
            clientes_data = obtener_todos_los_clientes()
            print(f"DEBUG: Cargando clientes, resultado: {len(clientes_data) if clientes_data else 0} clientes")
        except Exception as e:
            print(f"DEBUG: Error cargando clientes: {e}")
            self.status_label.setText(f"Error al cargar los clientes: {e}")
            self._mostrar_mensaje_error()
            return

        if not clientes_data:
            print("DEBUG: No hay clientes para mostrar")
            self._mostrar_mensaje_vacio()
            return

        # Renderizar directamente
        print(f"DEBUG: Renderizando {len(clientes_data)} clientes")
        self._clear_results()
        print(f"DEBUG: Después de clear_results, widgets en layout: {self.results_layout.count()}")
        for i, cliente in enumerate(clientes_data):
            print(f"DEBUG: Creando tarjeta {i+1} para cliente: {cliente.get('nombre_apellido', 'Sin nombre')}")
            card = TarjetaClienteQt(self.results_container, cliente)
            card.cliente_edit_requested.connect(self._editar_cliente)
            self.results_layout.addWidget(card)
        self.results_layout.addStretch(1)
        print(f"DEBUG: Final render, widgets en layout: {self.results_layout.count()}")

    # ---------- RENDER Y UTILIDADES ----------
    def _display_search_results_async(self, clientes_data: List[dict], search_term: str) -> None:
        def render():
            self._clear_results()
            if not clientes_data:
                self.status_label.setText(f"No se encontraron clientes con DNI '{search_term}'")
                self._mostrar_mensaje_vacio()
                return
            self.status_label.setText(f"Se encontraron {len(clientes_data)} cliente(s) con DNI '{search_term}'")
            for data in clientes_data:
                self.results_layout.addWidget(TarjetaClienteQt(self.results_container, data))
            self.results_layout.addStretch(1)
        self._invoke_in_main(render)

    def _mostrar_mensaje_vacio_async(self) -> None:
        self._invoke_in_main(self._mostrar_mensaje_vacio)

    def _mostrar_mensaje_error_async(self) -> None:
        def render():
            self._clear_results()
            msg = QLabel("Error al cargar los clientes")
            msg.setStyleSheet("color: orange; font-size: 18px;")
            self.results_layout.addWidget(msg)
        self._invoke_in_main(render)

    def _mostrar_mensaje_vacio(self) -> None:
        self._clear_results()
        msg = QLabel("No hay clientes registrados")
        msg.setStyleSheet("color: #bbbbbb; font-size: 18px;")
        self.results_layout.addWidget(msg)

    def _clear_results_async(self) -> None:
        self._invoke_in_main(self._clear_results)

    def _clear_results(self) -> None:
        print(f"DEBUG: Limpiando resultados, widgets actuales: {self.results_layout.count()}")
        while self.results_layout.count():
            item = self.results_layout.takeAt(0)
            w = item.widget()
            if w is not None:
                w.deleteLater()
        print(f"DEBUG: Después de limpiar, widgets: {self.results_layout.count()}")

    def _set_status_async(self, text: str) -> None:
        def set_text():
            self.status_label.setText(text)
        self._invoke_in_main(set_text)

    def _invoke_in_main(self, fn) -> None:
        QTimer.singleShot(0, fn)

    def _editar_cliente(self, dni: int) -> None:
        """Abre el diálogo de edición de cliente"""
        dialog = EditarClienteDialogQt(self, dni)
        if dialog.exec() == QDialog.Accepted:
            self.cargar_clientes()


__all__ = ["ClientesPage", "TarjetaClienteQt"]


