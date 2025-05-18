import customtkinter as ctk
import utils.util_ventana as utils_ventana
from view.components.modern_calendar import ModernCalendar
from config.db_queries import *
from datetime import datetime, date
from tkinter import messagebox
from tkcalendar import Calendar
from view.frames.interface.agregar_interface import BaseDialog

class AgregarTurnoDialog(BaseDialog):
    def __init__(self, parent, datos_iniciales=None, on_save=None):
        self.datos_iniciales = datos_iniciales or {}
        self.on_save = on_save
        super().__init__(parent, title="Nuevo Turno", width=700, height=600)

    def _create_form_widgets(self, master_frame):
        # DNI
        ctk.CTkLabel(master_frame, text="DNI del Cliente").pack(anchor="w", padx=10)
        self.entry_dni = ctk.CTkEntry(master_frame, placeholder_text="Ingrese DNI")
        self.entry_dni.pack(pady=5, padx=10, fill="x")
        self.entry_dni.insert(0, self.datos_iniciales.get("dni", ""))
        self.entry_dni.bind("<KeyRelease>", self.buscar_cliente_auto)

        # Nombre
        ctk.CTkLabel(master_frame, text="Nombre del Cliente").pack(anchor="w", padx=10)
        self.entry_nombre = ctk.CTkEntry(master_frame, placeholder_text="Ingrese nombre")
        self.entry_nombre.pack(pady=5, padx=10, fill="x")
        self.entry_nombre.insert(0, self.datos_iniciales.get("nombre", ""))

        # Servicio
        ctk.CTkLabel(master_frame, text="Servicio").pack(anchor="w", padx=10)
        self.combo_servicio = ctk.CTkComboBox(master_frame, values=["Modulo", "Vidrio", "Pin de carga", "Revisión", "Otros"])
        self.combo_servicio.pack(pady=5, padx=10, fill="x")
        if self.datos_iniciales.get("servicio"):
            self.combo_servicio.set(self.datos_iniciales["servicio"])
        else:
            self.combo_servicio.set("Seleccionar servicio")

        # Fecha (con botón para calendario)
        ctk.CTkLabel(master_frame, text="Fecha de Ingreso").pack(anchor="w", padx=10)
        fecha_frame = ctk.CTkFrame(master_frame, fg_color="transparent")
        fecha_frame.pack(pady=5, padx=10, fill="x")
        self.entry_fecha = ctk.CTkEntry(fecha_frame, placeholder_text="dd/mm/yyyy", width=180)
        self.entry_fecha.pack(side="left", fill="x", expand=True)
        self.entry_fecha.insert(0, self.datos_iniciales.get("fecha_ingreso", ""))

        btn_calendario = ctk.CTkButton(fecha_frame, text="📅", width=40, command=self.abrir_calendario)
        btn_calendario.pack(side="left", padx=5)

        # Presupuesto
        ctk.CTkLabel(master_frame, text="Presupuesto").pack(anchor="w", padx=10)
        self.entry_presupuesto = ctk.CTkEntry(master_frame, placeholder_text="Ingrese presupuesto")
        self.entry_presupuesto.pack(pady=5, padx=10, fill="x")
        self.entry_presupuesto.insert(0, self.datos_iniciales.get("presupuesto", ""))

        # Seña
        ctk.CTkLabel(master_frame, text="Seña").pack(anchor="w", padx=10)
        self.entry_sena = ctk.CTkEntry(master_frame, placeholder_text="Ingrese seña")
        self.entry_sena.pack(pady=5, padx=10, fill="x")
        self.entry_sena.insert(0, self.datos_iniciales.get("sena", ""))

        # Comentario
        ctk.CTkLabel(master_frame, text="Comentario").pack(anchor="w", padx=10)
        self.entry_comentario = ctk.CTkEntry(master_frame, placeholder_text="Comentario")
        self.entry_comentario.pack(pady=5, padx=10, fill="x")
        self.entry_comentario.insert(0, self.datos_iniciales.get("comentario", ""))

    def abrir_calendario(self):
        # Ventana emergente para seleccionar fecha
        top = ctk.CTkToplevel(self)
        top.title("Seleccionar fecha")
        cal = Calendar(top, selectmode='day', date_pattern='dd/mm/yyyy')
        cal.pack(padx=10, pady=10)

        def seleccionar_fecha():
            fecha = cal.get_date()
            self.entry_fecha.delete(0, ctk.END)
            self.entry_fecha.insert(0, fecha)
            top.destroy()

        ctk.CTkButton(top, text="Seleccionar", command=seleccionar_fecha).pack(pady=10)

    def _validate_form(self):
        if not self.entry_dni.get().strip():
            messagebox.showwarning("Campo obligatorio", "El DNI es obligatorio.")
            return False
        if not self.entry_nombre.get().strip():
            messagebox.showwarning("Campo obligatorio", "El nombre es obligatorio.")
            return False
        if self.combo_servicio.get() == "Seleccionar servicio":
            messagebox.showwarning("Campo obligatorio", "Debe seleccionar un servicio.")
            return False
        if not self.entry_fecha.get().strip():
            messagebox.showwarning("Campo obligatorio", "Debe seleccionar una fecha.")
            return False
        # Puedes agregar más validaciones aquí
        return True

    def _perform_save_action(self):
        datos = {
            "dni": self.entry_dni.get().strip(),
            "nombre": self.entry_nombre.get().strip(),
            "servicio": self.combo_servicio.get(),
            "fecha_ingreso": self.entry_fecha.get().strip(),
            "presupuesto": self.entry_presupuesto.get().strip(),
            "sena": self.entry_sena.get().strip(),
            "comentario": self.entry_comentario.get().strip(),
        }
        if self.on_save:
            self.on_save(datos)
        self.result = datos
        self.destroy()

    def buscar_cliente_auto(self, event=None):
        dni = self.entry_dni.get().strip()
        if len(dni) >= 4 and dni.isdigit():
            cliente = obtener_cliente(dni)
            if cliente:
                if isinstance(cliente, list):
                    cliente = cliente[0]  # Toma el primer cliente de la lista
                self.entry_nombre.delete(0, ctk.END)
                self.entry_nombre.insert(0, cliente.get("nombre", ""))
            else:
                # Si no se encuentra, puedes limpiar los campos o dejar el nombre vacío
                self.entry_nombre.delete(0, ctk.END)