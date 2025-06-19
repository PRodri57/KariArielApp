import customtkinter as ctk
from view.components.modern_calendar import ModernCalendar
from config.db_queries import *
from tkinter import messagebox
from tkcalendar import Calendar
from view.frames.interface.agregar_interface import BaseDialog
from model.TurnoV2 import TurnoV2
import threading
import time
from typing import List, Dict, Any

class AgregarTurnoDialog(BaseDialog):
    def __init__(self, parent, datos_iniciales=None, on_save=None):
        self.datos_iniciales = datos_iniciales or {}
        self.on_save = on_save
        
        # Variables para el search-as-you-type
        self.search_timer = None
        self.search_delay = 0.3  # 300ms de delay
        self.suggestions_window = None
        self.selected_cliente = None
        self.last_dni_text = ""  # Nuevo: para evitar búsquedas repetidas
        self.suggestions = []     # Nuevo: para selección con teclado
        self.suggestion_index = -1 # Nuevo: para selección con teclado
        
        super().__init__(parent, title="Nuevo Turno", width=700, height=600)

    def _create_form_widgets(self, master_frame):
        # *Numero de Orden
        ctk.CTkLabel(master_frame, text="Numero de Orden").pack(anchor="w", padx=10)
        self.entry_numero_orden = ctk.CTkEntry(master_frame, placeholder_text="Ingrese numero de orden")
        self.entry_numero_orden.pack(pady=5, padx=10, fill="x")
        self.entry_numero_orden.insert(0, self.datos_iniciales.get("numero_orden", ""))

        # *DNI con autocompletado
        ctk.CTkLabel(master_frame, text="DNI del Cliente").pack(anchor="w", padx=10)
        self.dni_frame = ctk.CTkFrame(master_frame, fg_color="transparent") # Frame para DNI y sugerencias
        self.dni_frame.pack(pady=5, padx=10, fill="x")

        self.entry_dni = ctk.CTkEntry(self.dni_frame, placeholder_text="Ingrese DNI para buscar")
        self.entry_dni.pack(fill="x")
        self.entry_dni.insert(0, self.datos_iniciales.get("dni", ""))

        # Vincular eventos para búsqueda automática
        self.entry_dni.bind("<KeyRelease>", self.on_dni_change)
        #self.entry_dni.bind("<FocusOut>", self.hide_suggestions)

        self.status_label = ctk.CTkLabel(master_frame, text="", font=ctk.CTkFont(size=11)) # Label para mostrar estado de búsqueda
        self.status_label.pack(anchor="w", padx=10)

        # *Telefono
        ctk.CTkLabel(master_frame, text="Telefono").pack(anchor="w", padx=10)
        self.entry_telefono = ctk.CTkEntry(master_frame, placeholder_text="Ingrese modelo del telefono")
        self.entry_telefono.pack(pady=5, padx=10, fill="x")
        self.entry_telefono.insert(0, self.datos_iniciales.get("telefono", ""))

        # *Nombre (se llenará automáticamente)
        ctk.CTkLabel(master_frame, text="Nombre del Cliente").pack(anchor="w", padx=10)
        self.entry_nombre = ctk.CTkEntry(master_frame, placeholder_text="Nombre del Cliente")
        self.entry_nombre.pack(pady=5, padx=10, fill="x")
        self.entry_nombre.insert(0, self.datos_iniciales.get("nombre", ""))

        # *Servicio
        ctk.CTkLabel(master_frame, text="Servicio").pack(anchor="w", padx=10)
        self.combo_servicio = ctk.CTkComboBox(master_frame, values=["Modulo", "Vidrio", "Pin de carga", "Revisión", "Otros"])
        self.combo_servicio.pack(pady=5, padx=10, fill="x")
        if self.datos_iniciales.get("servicio"):
            self.combo_servicio.set(self.datos_iniciales["servicio"])
        else:
            self.combo_servicio.set("Seleccionar servicio")

        # *Fecha (con botón para calendario)
        ctk.CTkLabel(master_frame, text="Fecha de Ingreso").pack(anchor="w", padx=10)
        fecha_frame = ctk.CTkFrame(master_frame, fg_color="transparent")
        fecha_frame.pack(pady=5, padx=10, fill="x")
        self.entry_fecha = ctk.CTkEntry(fecha_frame, placeholder_text="dd/mm/yyyy", width=180)
        self.entry_fecha.pack(side="left", fill="x", expand=True)
        self.entry_fecha.insert(0, self.datos_iniciales.get("fecha_ingreso", ""))

        btn_calendario = ctk.CTkButton(fecha_frame, text="📅", width=40, command=self.abrir_calendario)
        btn_calendario.pack(side="left", padx=5)

        # *Presupuesto
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

    def on_dni_change(self, event):
        """Se ejecuta cuando cambia el texto del DNI"""
        if self.search_timer:
            self.search_timer.cancel()
        dni_text = self.entry_dni.get().strip()
        # Nuevo: solo buscar si el texto cambió
        if dni_text == self.last_dni_text:
            return
        self.last_dni_text = dni_text
        if self.selected_cliente and self.selected_cliente.get('dni') != dni_text:
            self.selected_cliente = None
            if not dni_text:
                self.entry_nombre.delete(0, ctk.END)
        if len(dni_text) < 4:
            self.hide_suggestions()
            self.status_label.configure(text="")
            return
        self.status_label.configure(text="Buscando cliente...")
        self.search_timer = threading.Timer(
            self.search_delay,
            lambda: self.buscar_cliente_auto(dni_text)
        )
        self.search_timer.start()
        self.entry_dni.bind("<Down>", self.suggestion_down)
        self.entry_dni.bind("<Up>", self.suggestion_up)
        self.entry_dni.bind("<Return>", self.suggestion_select)

    def buscar_cliente_auto(self, dni_text: str):
        """Busca clientes en la base de datos"""
        try:
            from config.db_queries import obtener_cliente
            
            # Si no tienes esta función, aquí tienes un ejemplo de cómo implementarla:
            clientes = obtener_cliente(dni_text)
            
            # Nuevo: proteger si el texto cambió mientras se buscaba
            if dni_text != self.entry_dni.get().strip():
                return
            
            # Actualizar UI en el hilo principal
            self.after(0, lambda: self.mostrar_sugerencias(clientes, dni_text))
            
        except Exception as e:
            # Capturar el error en una variable local para evitar el problema de scope
            error_msg = str(e)
            self.after(0, lambda: self.mostrar_error(error_msg))

    def mostrar_sugerencias(self, clientes: List[Dict], dni_text: str):
        """Muestra las sugerencias de clientes encontrados"""
        self.hide_suggestions()
        
        self.suggestions = clientes  # Nuevo: guardar sugerencias para teclado
        self.suggestion_index = -1
        
        if not clientes:
            self.status_label.configure(text="No se encontraron clientes")
            return
        
        self.status_label.configure(text=f"Se encontraron {len(clientes)} cliente(s)")
        
        # Crear ventana de sugerencias
        self.suggestions_window = ctk.CTkToplevel(self)
        self.suggestions_window.title("Clientes encontrados")
        self.suggestions_window.geometry("400x300")
        self.suggestions_window.transient(self)
        self.suggestions_window.grab_set()

        # Nuevo: mejor posicionamiento
        x = self.entry_dni.winfo_rootx()
        y = self.entry_dni.winfo_rooty() + self.entry_dni.winfo_height() + 5
        self.suggestions_window.geometry(f"+{x}+{y}")
        
        # Frame principal para las sugerencias
        main_frame = ctk.CTkFrame(self.suggestions_window)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Título
        ctk.CTkLabel(main_frame, text="Selecciona un cliente:", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(10, 5))
        
        # Scrollable frame para las sugerencias
        suggestions_frame = ctk.CTkScrollableFrame(main_frame, height=200)
        suggestions_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Crear botón para cada cliente
        for idx, cliente in enumerate(clientes):
            self.crear_boton_cliente(suggestions_frame, cliente, idx)
        
        # Botón para cerrar
        ctk.CTkButton(main_frame, text="Cancelar", 
                     command=self.hide_suggestions).pack(pady=10)

    def crear_boton_cliente(self, parent, cliente: Dict, idx=None):
        """Crea un botón para cada cliente encontrado"""
        cliente_frame = ctk.CTkFrame(parent)
        cliente_frame.pack(fill="x", padx=5, pady=2)
        
        # Información del cliente
        info_text = f"DNI: {cliente.get('dni', 'N/A')} - {cliente.get('nombre_apellido', 'Sin nombre')}"
        if cliente.get('telefono'):
            info_text += f" - Tel: {cliente.get('telefono')}"
        
        btn_cliente = ctk.CTkButton(
            cliente_frame,
            text=info_text,
            command=lambda c=cliente: self.seleccionar_cliente(c),
            anchor="w",
            height=40
        )
        btn_cliente.pack(fill="x", padx=5, pady=5)
        # Nuevo: marcar el primer botón para selección con teclado
        if idx == 0:
            btn_cliente.focus_set()

    def seleccionar_cliente(self, cliente: Dict):
        """Selecciona un cliente y completa los campos"""
        self.selected_cliente = cliente
        
        # Completar campos
        self.entry_dni.delete(0, ctk.END)
        self.entry_dni.insert(0, cliente.get('dni', ''))
        
        self.entry_nombre.delete(0, ctk.END)
        self.entry_nombre.insert(0, cliente.get('nombre_apellido', ''))
        
        # Actualizar estado
        self.status_label.configure(text=f"Cliente seleccionado: {cliente.get('nombre_apellido', '')}")
        
        # Cerrar ventana de sugerencias
        self.hide_suggestions()

    def hide_suggestions(self, event=None):
        """Oculta la ventana de sugerencias"""
        if self.suggestions_window:
            self.suggestions_window.destroy()
            self.suggestions_window = None

    def mostrar_error(self, error_msg: str):
        """Muestra un error en la búsqueda"""
        self.status_label.configure(text=f"Error: {error_msg}")

    def abrir_calendario(self):
        # Ventana emergente para seleccionar fecha
        top = ctk.CTkToplevel(self)
        top.title("Seleccionar fecha")
        cal = Calendar(top, selectmode='day', date_pattern='dd/mm/yyyy')
        cal.pack(padx=10, pady=10)
        x = self.entry_fecha.winfo_rootx()
        y = self.entry_fecha.winfo_rooty() + self.entry_fecha.winfo_height() + 5
        top.geometry(f"+{x}+{y}")

        top.grab_set()

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
        return True

    def _perform_save_action(self):
        datos = {
            "numero_orden": self.entry_numero_orden.get().strip(),
            "dni": self.entry_dni.get().strip(),
            "telefono_id": self.entry_telefono.get().strip(),
            "nombre": self.entry_nombre.get().strip(),
            "servicio": self.combo_servicio.get(),
            "fecha_ingreso": self.entry_fecha.get().strip(),
            "presupuesto": self.entry_presupuesto.get().strip(),
            "sena": self.entry_sena.get().strip(),
            "comentario": self.entry_comentario.get().strip(),
        }

        if self.selected_cliente:
            datos["cliente_info"] = self.selected_cliente

        try:
            turno = TurnoV2.from_dict(datos)
        except Exception as e:
            messagebox.showerror("Error al crear el turno", f"Datos inválidos: {e}")
            return

        if self.on_save:
            self.on_save(turno.to_dict())
        self.result = turno.to_dict()
        self.destroy()

    def destroy(self):
        if self.search_timer:
            self.search_timer.cancel()
        if self.suggestions_window:
            self.suggestions_window.destroy()
        super().destroy()

    def suggestion_down(self, event):
        if not self.suggestions:
            return
        self.suggestion_index = (self.suggestion_index + 1) % len(self.suggestions)

    def suggestion_up(self, event):
        if not self.suggestions:
            return
        self.suggestion_index = (self.suggestion_index - 1) % len(self.suggestions)

    def suggestion_select(self, event):
        if self.suggestions and 0 <= self.suggestion_index < len(self.suggestions):
            self.seleccionar_cliente(self.suggestions[self.suggestion_index])
