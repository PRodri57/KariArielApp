import customtkinter as ctk
from view.components.modern_calendar import ModernCalendar
from config.supabase_client import supabase
from utils.offline_cache import obtener_turnos_locales
from datetime import datetime, date
from tkinter import messagebox
import socket
from config.db_queries import *
from .subframes.agregar_turno_frame import *

class TurnosFrame(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.contenedor_secundario = ctk.CTkFrame(self, fg_color="#252525", border_color="#252525")

        btn_nuevo_turno = ctk.CTkButton(
            self, text="➕ Nuevo Turno", width=150,
            command=self.abrir_formulario_nuevo_turno)
        btn_nuevo_turno.pack(pady=10, padx=10, anchor="ne")

        self.calendario = ModernCalendar(
            self.contenedor_secundario,
            on_select=self.actualizar_fecha_seleccionada
        )

        self.label_turnos = ctk.CTkLabel(self, text=f"Turnos del día {self.calendario.get_date()}", font=("Bahnschrift", 40))
        self.label_turnos.pack(pady=10, anchor="n")
        

        self.contenedor_secundario.pack(expand=True, fill="both", padx=20, pady=10)
        self.calendario.grid(row=0, column=0, padx=20, pady=10)

        self.scroll_frame = ctk.CTkScrollableFrame(self.contenedor_secundario, width=800, height=500, corner_radius=32, 
                                                    fg_color="#252525", border_color="#252525")
        self.scroll_frame.grid(row=0, column=1, padx=20, pady=10, sticky="nsew")

        self.cargar_turnos(date.today().isoformat())
    
    def actualizar_fecha_seleccionada(self, fecha):
        self.fecha_seleccionada = fecha.strftime("%d/%m/%Y")
        self.label_turnos.configure(text=f"Turnos del día {self.fecha_seleccionada}")
        self.cargar_turnos(fecha.isoformat())

    def abrir_formulario_nuevo_turno(self):
        dialog = AgregarTurnoDialog(self.winfo_toplevel())
        self.wait_window(dialog)
        self.cargar_turnos()

    @staticmethod
    def hay_internet():
        try:
            socket.create_connection(("1.1.1.1", 53), timeout=3)
            return True
        except OSError:
            return False

    def obtener_turnos_del_dia(self, fecha_iso=None):
        if fecha_iso is None:
            fecha_iso = date.today().isoformat()
        turnos = obtener_turnos_por_fecha(fecha_iso)
        if turnos is not None:
            return turnos
        return [t for t in obtener_turnos_locales() if t["fecha"] == fecha_iso]

    def cargar_turnos(self, fecha_iso=None):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        turnos = self.obtener_turnos_del_dia(fecha_iso)

        if not turnos:
            ctk.CTkLabel(
                self.scroll_frame,
                text="No hay turnos para esta fecha.",
                font=("Bahnschrift", 16)
            ).pack(pady=5, anchor="w")
            return

        for turno in turnos:
            frame_turno = ctk.CTkFrame(
                self.scroll_frame,
                fg_color="#333333",
                corner_radius=10,
                border_width=1,
                border_color="#555555"
            )
            frame_turno.pack(pady=10, padx=10, fill="x")

            # Info principal
            ctk.CTkLabel(
                frame_turno,
                text=f"Orden {turno['numero_orden']} - ({turno['tipo_servicio']})",
                font=("Bahnschrift", 20, "bold")
            ).pack(padx=15, pady=10, anchor="w")

            # Info adicional (opcional)
            if "tecnico" in turno:
                detalles = ""
                if "tecnico" in turno:
                    detalles += f"Técnico: {turno['tecnico']}"

                ctk.CTkLabel(
                    frame_turno,
                    text=detalles,
                    font=("Arial", 12),
                    text_color="#bbb"
                ).pack(padx=15, pady=(0, 10), anchor="w")

            # Hacer que sea seleccionable
            frame_turno.bind("<Button-1>", lambda e, t=turno: self.seleccionar_turno(t))
            frame_turno.bind("<Enter>", lambda e: frame_turno.configure(fg_color="#444444"))
            frame_turno.bind("<Leave>", lambda e: frame_turno.configure(fg_color="#333333"))

    def seleccionar_turno(self, turno):
        print("Turno seleccionado:", turno)
        messagebox.showinfo("Turno", f"Cliente: {turno['numero_orden']}\nServicio: {turno['tipo_servicio']}")
    
