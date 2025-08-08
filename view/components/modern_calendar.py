# modern_calendar.py
import customtkinter as ctk
from datetime import datetime, timedelta

class ModernCalendar(ctk.CTkFrame):
    def __init__(self, parent, on_select=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.on_select = on_select  # Callback al hacer click en una fecha
        self.fecha_actual = datetime.now()
        self.day_buttons = {}
        self.selected_day = None

        self.configure(fg_color="transparent")
        self.build_ui()
        self.update_calendar()

    def build_ui(self):
        # Encabezado: mes y año
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(pady=10)

        self.btn_prev = ctk.CTkButton(header_frame, text="◀", width=30, command=self.mes_anterior)
        self.btn_prev.pack(side="left")

        self.lbl_mes = ctk.CTkLabel(header_frame, text="", font=("Segoe UI", 16, "bold"))
        self.lbl_mes.pack(side="left", padx=20)

        self.btn_next = ctk.CTkButton(header_frame, text="▶", width=30, command=self.mes_siguiente)
        self.btn_next.pack(side="left")

        # Días de la semana
        dias_frame = ctk.CTkFrame(self, fg_color="transparent")
        dias_frame.pack(fill="x", padx=10)

        for i, dia in enumerate(["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]):
            ctk.CTkLabel(dias_frame, text=dia, width=50, anchor="center").grid(row=0, column=i, padx=2, pady=5)

        # Grid de días
        self.dias_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.dias_frame.pack(fill="both", expand=True)

    def update_calendar(self):
        """Actualiza los días del mes actual"""
        for widget in self.dias_frame.winfo_children():
            widget.destroy()

        self.day_buttons = {}

        year = self.fecha_actual.year
        month = self.fecha_actual.month

        self.lbl_mes.configure(text=f"{self.fecha_actual.strftime('%B')} {year}")

        # Obtener primer día del mes y cantidad de días
        primer_dia = datetime(year, month, 1).weekday()  # Lunes = 0 ... Domingo = 6
        dias_en_mes = (datetime(year, month + 1, 1) - timedelta(days=1)).day if month < 12 else 31

        # Ajuste para que empiece desde lunes
        offset = (primer_dia + 1) % 7  # Aseguramos que lunes sea posición 0

        for i in range(42):  # 6 semanas x 7 días
            fila = i // 7
            columna = i % 7

            dia = i - offset + 1
            if 1 <= dia <= dias_en_mes:
                btn = ctk.CTkButton(
                    self.dias_frame,
                    text=str(dia),
                    width=50,
                    height=40,
                    corner_radius=8,
                    fg_color="transparent",
                    hover_color="#005F9E",
                    command=lambda d=dia: self.seleccionar_fecha(d)
                )
                btn.grid(row=fila, column=columna, padx=2, pady=2)
                self.day_buttons[dia] = btn
            else:
                # Espacio vacío
                ctk.CTkLabel(self.dias_frame, text="", width=50).grid(
                    row=fila, column=columna, padx=2, pady=2
                )

        # Selección por defecto: día actual si el mes/año coinciden con hoy
        hoy = datetime.now()
        if (self.fecha_actual.year == hoy.year and self.fecha_actual.month == hoy.month):
            if self.selected_day is None:
                self.selected_day = hoy.day

        self._apply_selection_style()

    def mes_anterior(self):
        self.fecha_actual -= timedelta(days=1)
        self.fecha_actual = datetime(self.fecha_actual.year, self.fecha_actual.month, 1)
        self.selected_day = None
        self.update_calendar()

    def mes_siguiente(self):
        next_month = self.fecha_actual.replace(day=28) + timedelta(days=4)
        self.fecha_actual = datetime(next_month.year, next_month.month, 1)
        self.selected_day = None
        self.update_calendar()

    def seleccionar_fecha(self, dia):
        self.selected_day = dia
        self._apply_selection_style()
        fecha_seleccionada = datetime(self.fecha_actual.year, self.fecha_actual.month, dia)
        if self.on_select:
            self.on_select(fecha_seleccionada)

    def get_date(self):
        return self.fecha_actual.strftime("%Y-%m-%d")

    def _apply_selection_style(self):
        """Actualiza el estilo visual del día seleccionado."""
        for d, btn in self.day_buttons.items():
            if d == self.selected_day:
                btn.configure(fg_color="#0A84FF", hover_color="#0A84FF", text_color="white")
            else:
                btn.configure(fg_color="transparent", hover_color="#005F9E")

# Si quieres probarlo directamente:
if __name__ == "__main__":
    app = ctk.CTk()
    def mostrar_fecha(fecha):
        print("Fecha seleccionada:", fecha.strftime("%d/%m/%Y"))

    cal = ModernCalendar(app, on_select=mostrar_fecha)
    cal.pack(padx=20, pady=20)
    app.mainloop()