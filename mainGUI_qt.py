from __future__ import annotations
from PySide6.QtCore import Qt, QSize, Signal
from PySide6.QtGui import QIcon, QAction, QPalette, QColor, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QStackedWidget,
    QLabel,
    QFrame,
)
import sys
from view.frames.turnos_page_qt import TurnosPage
from view.frames.clientes_page_qt import ClientesPage
from view.frames.telefonos_page_qt import TelefonosPage


def apply_dark_palette(app: QApplication) -> None:
    """Aplica un tema oscuro estilo Fusion de manera simple."""
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(35, 35, 35))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)


class Sidebar(QFrame):
    navigate = Signal(str)  # Emite: "inicio" | "turnos" | "clientes" | "presupuesto"

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("Sidebar")
        self.setFixedWidth(220)
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)

        # Botones de navegación
        self.btn_inicio = self._create_nav_button("Inicio", "inicio")
        self.btn_turnos = self._create_nav_button("Turnos", "turnos")
        self.btn_clientes = self._create_nav_button("Clientes", "clientes")
        self.btn_presupuesto = self._create_nav_button("Presupuesto", "presupuesto")
        self.btn_telefonos = self._create_nav_button("Teléfonos", "telefonos")

        for btn in [self.btn_inicio, self.btn_turnos, self.btn_clientes, self.btn_presupuesto, self.btn_telefonos]:
            layout.addWidget(btn)

        layout.addStretch(1)

        self.setStyleSheet(
            """
            QFrame#Sidebar { background-color: #2b2b2b; }
            QPushButton { 
                color: #ffffff; background-color: #3a3a3a; border: 1px solid #444; 
                padding: 10px; border-radius: 6px; text-align: left; 
            }
            QPushButton:hover { background-color: #454545; }
            QPushButton:pressed { background-color: #2f2f2f; }
            """
        )

    def _create_nav_button(self, text: str, key: str) -> QPushButton:
        btn = QPushButton(text)
        btn.setCursor(Qt.PointingHandCursor)
        btn.clicked.connect(lambda: self.navigate.emit(key))
        btn.setIconSize(QSize(18, 18))
        return btn


class SimplePage(QWidget):
    def __init__(self, title: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        label = QLabel(title)
        label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        label.setStyleSheet("QLabel { font-size: 24px; font-weight: 600; }")
        layout.addWidget(label)

        # Espacio para contenido futuro (migración de frames específicos)
        placeholder = QLabel("En proceso...")
        placeholder.setStyleSheet("color: #bbbbbb;")
        layout.addWidget(placeholder)
        layout.addStretch(1)


class HomePage(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)
        layout.setAlignment(Qt.AlignCenter)

        image_label = QLabel()
        image_label.setAlignment(Qt.AlignCenter)
        try:
            pix = QPixmap("assets/icono.png")
            if not pix.isNull():
                pix = pix.scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                image_label.setPixmap(pix)
        except Exception:
            pass
        layout.addWidget(image_label)

        title = QLabel("Bienvenido/a a KariAriel")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("QLabel { font-size: 40px; font-weight: 700; font-family: 'Bahnschrift', sans-serif; }")
        layout.addWidget(title)


class AppPrincipalQt(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        # Ventana principal
        self.setWindowTitle("KariAriel (Qt)")
        try:
            self.setWindowIcon(QIcon("assets/icono.ico"))
        except Exception:
            pass
        self.resize(1366, 768)

        # Contenedor central con layout horizontal: Sidebar | Stacked
        central = QWidget(self)
        self.setCentralWidget(central)
        h_layout = QHBoxLayout(central)
        h_layout.setContentsMargins(0, 0, 0, 0)
        h_layout.setSpacing(0)

        # Sidebar
        self.sidebar = Sidebar(self)
        h_layout.addWidget(self.sidebar)

        # Stacked (páginas)
        self.stacked = QStackedWidget(self)
        self.stacked.setObjectName("StackedPages")
        h_layout.addWidget(self.stacked, 1)

        # Páginas
        self.page_home = HomePage()
        self.page_turnos = TurnosPage()
        self.page_clientes = ClientesPage()
        self.page_presupuesto = SimplePage("Presupuesto")
        self.page_telefonos = TelefonosPage()

        self.page_key_to_index = {
            "inicio": self.stacked.addWidget(self.page_home),
            "turnos": self.stacked.addWidget(self.page_turnos),
            "clientes": self.stacked.addWidget(self.page_clientes),
            "presupuesto": self.stacked.addWidget(self.page_presupuesto),
            "telefonos": self.stacked.addWidget(self.page_telefonos),
        }

        # Conexiones
        self.sidebar.navigate.connect(self._on_navigate)

        # Página inicial
        self._on_navigate("inicio")

        # Estilos básicos del contenedor
        self.setStyleSheet(
            """
            QStackedWidget#StackedPages { background-color: #1f1f1f; }
            """
        )

        # Centrado en pantalla
        self._center_on_screen()

    def _center_on_screen(self) -> None:
        screen = self.screen() or self.windowHandle().screen() if self.windowHandle() else None
        if screen is None:
            return
        geo = self.frameGeometry()
        geo.moveCenter(screen.availableGeometry().center())
        self.move(geo.topLeft())

    def _on_navigate(self, key: str) -> None:
        index = self.page_key_to_index.get(key, 0)
        self.stacked.setCurrentIndex(index)


def main() -> None:
    app = QApplication(sys.argv)
    apply_dark_palette(app)
    window = AppPrincipalQt()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()


