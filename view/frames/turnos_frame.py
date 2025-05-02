import customtkinter as ctk
import tkcalendar as Calendar
from supabase_client import supabase
from datetime import date

class TurnosFrame(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.calendario = Calendar.Calendar(self, selectmode='day', date_pattern='dd/mm/yyyy', showweeknumbers=False,
                                             firstweekday='sunday', locale='es_ES', showothermonthdays=False,
                                             background="#252525", disabledbackground="#252525", bordercolor="#252525",
                                             headersbackground="#252525", normalbackground="#252525",
                                             foreground="#ffffff", normalforeground="#cfcfd4", headersforeground="#ffffff",
                                             weekendbackground="#252525", weekendforeground="#ffffff",
                                             selectbackground="#003e6f", othermonthbackground="#252525",
                                             othermonthforeground="#6c6c80")
        self.label_turnos = ctk.CTkLabel(self, text=f"Turnos del día {self.calendario.get_date()}",
                                         font=("Bahnschrift", 40))

        self.label_turnos.pack(pady=10)
        self.calendario.pack(expand=True, fill="both", padx=20, pady=10)

        self.calendario.bind("<<CalendarSelected>>", self._on_fecha_seleccionada)

        self.scroll_frame = ctk.CTkScrollableFrame(self, width=600, height=400)
        self.scroll_frame.pack(pady=10)

        self.cargar_turnos()

    def _on_fecha_seleccionada(self, event=None):
        fecha = self.calendario.selection_get()
        self.label_turnos.configure(text=f"Turnos del día {fecha}")

    def obtener_turnos_del_dia(self):
        hoy = date.today().isoformat()
        response = supabase.table("turnos").select("*").eq("fecha_hora", hoy).execute()
        return response.data

    def cargar_turnos(self):
        turnos = self.obtener_turnos_del_dia()
        for i, turno in enumerate(turnos):
            texto = f"{turno['hora']} - {turno['cliente']} ({turno['servicio']})"
            label = ctk.CTkLabel(self.scroll_frame, text=texto, font=("Bahnschrift", 16))
            label.pack(pady=5, anchor="w")