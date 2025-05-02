import customtkinter as ctk
from tkcalendar import Calendar
from datetime import datetime

class PresupuestoFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        self.grid_columnconfigure(0, weight=1)

        # Etiqueta principal
        self.label_presupuesto = ctk.CTkLabel(
            self,
            text=f"Proximamente...",
            font=("Bahnschrift", 40, "italic"),
        )
        self.label_presupuesto.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        # Calendario
        """ self.calendario = Calendar.Calendar(self, selectmode='day', date_pattern='dd/mm/yyyy', showweeknumbers=False,
                                             firstweekday='sunday', locale='es_ES', showothermonthdays=False,
                                             background="#252525", disabledbackground="#252525", bordercolor="#252525",
                                             headersbackground="#252525", normalbackground="#252525",
                                             foreground="#ffffff", normalforeground="#cfcfd4", headersforeground="#ffffff",
                                             weekendbackground="#252525", weekendforeground="#ffffff",
                                             selectbackground="#003e6f", othermonthbackground="#252525",
                                             othermonthforeground="#6c6c80")
        self.calendario.pack(expand=True, fill="both", padx=20, pady=10)

        self.calendario.bind("<<CalendarSelected>>", self._on_fecha_seleccionada)
 """
    def _on_fecha_seleccionada(self, event=None):
        fecha = self.calendario.selection_get()
        self.label_presupuesto.configure(text=f"Presupuesto del día {fecha}")
