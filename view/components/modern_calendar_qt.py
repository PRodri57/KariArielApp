from __future__ import annotations

from datetime import datetime, timedelta
from calendar import monthrange

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QGridLayout,
    QFrame,
)


class ModernCalendarQt(QFrame):
    """
    Calendario estilo "moderno" en PySide6, compatible conceptualmente con ModernCalendar (Tk).

    API compatible clave:
      - on_select: callback(datetime) al seleccionar un día
      - seleccionar_fecha(dia: int)
      - get_date() -> str (YYYY-MM-DD del mes/año visibles)
    """

    def __init__(self, parent: QWidget | None = None, on_select=None, **kwargs) -> None:
        super().__init__(parent)
        self.on_select = on_select
        self.fecha_actual = datetime.now()
        self.day_buttons: dict[int, QPushButton] = {}
        self.selected_day: int | None = None

        self.setObjectName("ModernCalendarQt")
        self.setStyleSheet(
            """
            QFrame#ModernCalendarQt { background: transparent; }
            QLabel[role="dow"] { color: #ddd; }
            QPushButton[role="nav"] { min-width: 30px; padding: 6px 10px; }
            QPushButton[role="nav"]:hover { background: #454545; }
            QLabel[role="title"] { font-size: 16px; font-weight: 600; }
            """
        )

        self._build_ui()
        self.update_calendar()

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(8)

        # Encabezado: mes y año
        header = QHBoxLayout()
        header.setSpacing(8)

        self.btn_prev = QPushButton("◀")
        self.btn_prev.setProperty("role", "nav")
        self.btn_prev.clicked.connect(self.mes_anterior)
        header.addWidget(self.btn_prev)

        self.lbl_mes = QLabel("")
        self.lbl_mes.setProperty("role", "title")
        header.addWidget(self.lbl_mes, 1, alignment=Qt.AlignCenter)

        self.btn_next = QPushButton("▶")
        self.btn_next.setProperty("role", "nav")
        self.btn_next.clicked.connect(self.mes_siguiente)
        header.addWidget(self.btn_next)

        root.addLayout(header)

        # Días de la semana
        dow = QHBoxLayout()
        dow.setSpacing(4)
        for dia in ["Dom", "Lun", "Mar", "Mié", "Jue", "Vie", "Sáb"]:
            l = QLabel(dia)
            l.setProperty("role", "dow")
            l.setAlignment(Qt.AlignCenter)
            l.setFixedWidth(50)
            dow.addWidget(l)
        root.addLayout(dow)

        # Grid de días
        self.grid_container = QFrame(self)
        self.grid_container.setObjectName("gridContainer")
        self.grid_container.setStyleSheet("QFrame#gridContainer { background: transparent; }")
        root.addWidget(self.grid_container)

        self.grid_days = QGridLayout(self.grid_container)
        self.grid_days.setContentsMargins(0, 0, 0, 0)
        self.grid_days.setHorizontalSpacing(4)
        self.grid_days.setVerticalSpacing(4)

    def update_calendar(self) -> None:
        # Limpiar grid
        for i in reversed(range(self.grid_days.count())):
            item = self.grid_days.itemAt(i)
            w = item.widget()
            if w is not None:
                w.deleteLater()
            self.grid_days.removeItem(item)
        self.day_buttons.clear()

        year = self.fecha_actual.year
        month = self.fecha_actual.month

        self.lbl_mes.setText(f"{self.fecha_actual.strftime('%B')} {year}")

        # Primer día del mes y cantidad de días
        primer_dia = datetime(year, month, 1).weekday()  # Lunes = 0 ... Domingo = 6
        dias_en_mes = monthrange(year, month)[1]

        # Ajuste para que empiece desde Domingo
        offset = (primer_dia + 1) % 7

        for i in range(42):  # 6 semanas x 7 días
            fila = i // 7
            columna = i % 7
            dia = i - offset + 1

            if 1 <= dia <= dias_en_mes:
                btn = QPushButton(str(dia), self.grid_container)
                btn.setFixedSize(50, 40)
                btn.setProperty("role", "day")
                btn.setStyleSheet(
                    "QPushButton { background: transparent; border-radius: 8px; }"
                    "QPushButton:hover { background: #005F9E; color: white; }"
                )
                btn.clicked.connect(lambda _=False, d=dia: self.seleccionar_fecha(d))
                self.grid_days.addWidget(btn, fila, columna)
                self.day_buttons[dia] = btn
            else:
                spacer = QLabel("")
                spacer.setFixedSize(50, 40)
                self.grid_days.addWidget(spacer, fila, columna)

        # Selección por defecto: día actual si el mes/año coinciden con hoy
        hoy = datetime.now()
        if self.fecha_actual.year == hoy.year and self.fecha_actual.month == hoy.month:
            if self.selected_day is None:
                self.selected_day = hoy.day

        self._apply_selection_style()

    def mes_anterior(self) -> None:
        self.fecha_actual -= timedelta(days=1)
        self.fecha_actual = datetime(self.fecha_actual.year, self.fecha_actual.month, 1)
        self.selected_day = None
        self.update_calendar()

    def mes_siguiente(self) -> None:
        next_month = self.fecha_actual.replace(day=28) + timedelta(days=4)
        self.fecha_actual = datetime(next_month.year, next_month.month, 1)
        self.selected_day = None
        self.update_calendar()

    def seleccionar_fecha(self, dia: int) -> None:
        self.selected_day = dia
        self._apply_selection_style()
        fecha_seleccionada = datetime(self.fecha_actual.year, self.fecha_actual.month, dia)
        if self.on_select:
            self.on_select(fecha_seleccionada)

    def get_date(self) -> str:
        """Devuelve YYYY-MM-DD del mes visible (día = seleccionado o 1)."""
        day = self.selected_day if self.selected_day is not None else 1
        return datetime(self.fecha_actual.year, self.fecha_actual.month, day).strftime("%Y-%m-%d")

    def get_selected_date(self) -> datetime:
        """Devuelve la fecha seleccionada como datetime (si no hay selección, usa día 1)."""
        day = self.selected_day if self.selected_day is not None else 1
        return datetime(self.fecha_actual.year, self.fecha_actual.month, day)

    def get_selected_date_iso(self) -> str:
        """Devuelve la fecha seleccionada en formato ISO (YYYY-MM-DD)."""
        return self.get_selected_date().date().isoformat()

    def _apply_selection_style(self) -> None:
        for d, btn in self.day_buttons.items():
            if d == self.selected_day:
                btn.setStyleSheet(
                    "QPushButton { background: #0A84FF; color: white; border-radius: 8px; }"
                )
            else:
                btn.setStyleSheet(
                    "QPushButton { background: transparent; border-radius: 8px; }"
                    "QPushButton:hover { background: #005F9E; color: white; }"
                )


__all__ = ["ModernCalendarQt"]


