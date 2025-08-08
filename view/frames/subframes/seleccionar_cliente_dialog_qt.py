from __future__ import annotations

from typing import List, Dict, Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QFrame,
    QWidget,
    QDialogButtonBox,
)

from model.Clientes import Cliente


class TarjetaClienteSeleccionQt(QFrame):
    def __init__(self, parent: QWidget | None, cliente_data: dict, on_select=None, is_single_client=False) -> None:
        super().__init__(parent)
        self.setObjectName("TarjetaClienteSeleccion")
        self.on_select = on_select
        self.cliente_data = cliente_data
        self.is_single_client = is_single_client
        
        self.setStyleSheet(
            """
            QFrame#TarjetaClienteSeleccion { 
                background: #2c2c2c; 
                border: 1px solid #3a3a3a; 
                border-radius: 8px; 
                margin: 2px;
            }
            QFrame#TarjetaClienteSeleccion:hover { 
                background: #3a3a3a; 
                border: 1px solid #555;
            }
            QLabel[role="name"] { font-size: 16px; font-weight: 700; }
            QLabel[role="meta"] { color: #bbbbbb; font-size: 12px; }
            QPushButton { 
                background: #4a4a4a; 
                border: 1px solid #555; 
                border-radius: 4px; 
                padding: 6px 12px; 
                color: #fff;
            }
            QPushButton:hover { background: #5a5a5a; }
            """
        )

        cliente = Cliente.from_dict(cliente_data)

        root = QVBoxLayout(self)
        root.setContentsMargins(12, 10, 12, 10)
        root.setSpacing(4)

        # Primera fila: Nombre y botón seleccionar
        header = QHBoxLayout()
        
        nombre = QLabel(cliente.nombre_apellido)
        nombre.setProperty("role", "name")
        header.addWidget(nombre)
        
        header.addStretch(1)
        
        # Cambiar texto del botón según si hay uno o varios clientes
        if self.is_single_client:
            btn_text = "Confirmar"
        else:
            btn_text = "Seleccionar"
        
        btn_seleccionar = QPushButton(btn_text)
        btn_seleccionar.setFixedWidth(80)
        btn_seleccionar.clicked.connect(self._on_seleccionar)
        header.addWidget(btn_seleccionar)
        
        root.addLayout(header)

        # DNI
        dni = QLabel(f"DNI: {cliente.dni}")
        dni.setProperty("role", "meta")
        root.addWidget(dni)

        # Teléfono (si existe)
        if cliente.telefono:
            telefono = QLabel(f"Teléfono: {cliente.telefono}")
            telefono.setProperty("role", "meta")
            root.addWidget(telefono)

        # Email (si existe)
        if cliente.email:
            email = QLabel(f"Email: {cliente.email}")
            email.setProperty("role", "meta")
            root.addWidget(email)

        # Dirección (si existe)
        if cliente.direccion:
            direccion = QLabel(f"Dirección: {cliente.direccion}")
            direccion.setProperty("role", "meta")
            root.addWidget(direccion)

    def _on_seleccionar(self) -> None:
        if self.on_select:
            self.on_select(self.cliente_data)


class SeleccionarClienteDialogQt(QDialog):
    def __init__(self, parent: QWidget | None, clientes: List[dict], search_term: str) -> None:
        super().__init__(parent)
        self.setWindowTitle("Seleccionar Cliente")
        self.resize(500, 400)
        self.setModal(True)
        
        self.clientes = clientes
        self.search_term = search_term
        self.selected_cliente: Optional[dict] = None
        
        self._build_ui()

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(16, 16, 16, 16)
        root.setSpacing(12)

        # Título
        if len(self.clientes) == 1:
            titulo = QLabel(f"Se encontró 1 cliente con DNI '{self.search_term}'")
        else:
            titulo = QLabel(f"Se encontraron {len(self.clientes)} cliente(s) con DNI '{self.search_term}'")
        titulo.setStyleSheet("QLabel { font-size: 18px; font-weight: 700; }")
        root.addWidget(titulo)

        # Subtítulo
        if len(self.clientes) == 1:
            subtitulo = QLabel("Confirma que es el cliente correcto:")
        else:
            subtitulo = QLabel("Selecciona el cliente correcto:")
        subtitulo.setStyleSheet("QLabel { color: #bbbbbb; font-size: 14px; }")
        root.addWidget(subtitulo)

        # Scroll area para las tarjetas
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.NoFrame)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        root.addWidget(self.scroll_area, 1)

        # Contenedor de resultados
        self.results_container = QWidget()
        self.results_layout = QVBoxLayout(self.results_container)
        self.results_layout.setContentsMargins(8, 8, 8, 8)
        self.results_layout.setSpacing(8)
        self.results_layout.setAlignment(Qt.AlignTop)
        self.scroll_area.setWidget(self.results_container)

        # Botones
        buttons = QDialogButtonBox(QDialogButtonBox.Cancel)
        buttons.rejected.connect(self.reject)
        root.addWidget(buttons)

        # Estilo
        self.setStyleSheet(
            """
            QDialog { background: #1f1f1f; color: #ffffff; }
            QScrollArea { background: #1f1f1f; border: none; }
            """
        )

        # Renderizar clientes
        self._render_clientes()

    def _render_clientes(self) -> None:
        for cliente in self.clientes:
            card = TarjetaClienteSeleccionQt(
                self.results_container, 
                cliente, 
                on_select=self._on_cliente_selected,
                is_single_client=(len(self.clientes) == 1)
            )
            self.results_layout.addWidget(card)
        
        self.results_layout.addStretch(1)

    def _on_cliente_selected(self, cliente: dict) -> None:
        self.selected_cliente = cliente
        self.accept()

    def get_selected_cliente(self) -> Optional[dict]:
        return self.selected_cliente


__all__ = ["SeleccionarClienteDialogQt", "TarjetaClienteSeleccionQt"]
