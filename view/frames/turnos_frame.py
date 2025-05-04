import customtkinter as ctk
import tkcalendar
from view.components.modern_calendar import ModernCalendar
from config.supabase_client import supabase, insertar_con_respaldo
from utils.offline_cache import obtener_turnos_locales
import utils.util_ventana as utils_ventana
from datetime import datetime, date
from tkinter import messagebox
import socket


class TurnosFrame(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.contenedor_secundario = ctk.CTkFrame(self, fg_color="#252525", border_color="#252525")

        btn_nuevo_turno = ctk.CTkButton(
            self, text="➕ Nuevo Turno", width=150,
            command=self.abrir_formulario_nuevo_turno)
        btn_nuevo_turno.pack(pady=10, anchor="ne")

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
        dialog = NuevoTurnoDialog(self.winfo_toplevel())
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

        print(f"[DEBUG] Buscando turnos para fecha ISO: {fecha_iso}")

        if self.hay_internet():
            try:
                response = supabase.table("Telefonos").select("*").eq("fecha", fecha_iso).execute()
                #print("Turnos encontrados:", response.data)
                #print("[DEBUG] Respuesta completa:", response)  # 👈 Ver qué trae
                #print("[DEBUG] Datos recibidos:", response.data)  # 👈 Ver si hay datos
                return response.data
            except Exception as e:
                print("[ERROR] Fallo al conectar con Supabase:", str(e))
        
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
                text=f"{turno.get('hora', 'Sin hora')} - {turno['numeroOrden']} ({turno['servicio']})",
                font=("Bahnschrift", 20, "bold")
            ).pack(padx=15, pady=10, anchor="w")

            # Info adicional (opcional)
            if "tecnico" in turno:
                detalles = ""
                if "tecnico" in turno:
                    detalles += f"Técnico: {turno['tecnico']} | "

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
        messagebox.showinfo("Turno", f"Cliente: {turno['numeroOrden']}\nServicio: {turno['servicio']}")
    
class NuevoTurnoDialog(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Nuevo Turno")
        h, w = 720, 1200
        utils_ventana.centrar_ventana(self, w, h)
        #self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        self.contenedor = ctk.CTkFrame(self)
        self.contenedor.pack(pady=20, padx=30, fill="both", expand=True)

        # Título
        ctk.CTkLabel(self.contenedor, text="Registrar Nuevo Turno", font=("Arial", 20, "bold")).pack(pady=(0, 20))

        # Campo DNI
        ctk.CTkLabel(self.contenedor, text="DNI del Cliente", font=("Arial", 12)).pack(anchor="w", padx=10)
        self.entry_dni = ctk.CTkEntry(self.contenedor, placeholder_text="Buscar por DNI")
        self.entry_dni.pack(pady=5, padx=10, fill="x")

        ctk.CTkButton(self.contenedor, text="Buscar Cliente", command=self.buscar_cliente).pack(pady=5)

        # Datos del cliente (no editables)
        self.frame_datos_cliente = ctk.CTkFrame(self.contenedor, fg_color="transparent")
        self.frame_datos_cliente.pack(fill="x", pady=10)

        self.label_nombre = ctk.CTkLabel(self.frame_datos_cliente, text="", anchor="w")
        self.label_telefono = ctk.CTkLabel(self.frame_datos_cliente, text="", anchor="w")
        self.label_email = ctk.CTkLabel(self.frame_datos_cliente, text="", anchor="w")

        for label in [self.label_nombre, self.label_telefono, self.label_email]:
            label.pack(anchor="w", padx=10)

        # Selector de fecha integrado
        self.calendario = ModernCalendar(
            self.contenedor,
            on_select=self.actualizar_fecha_seleccionada
        )
        self.calendario.pack(pady=10, fill="x")

        # Servicio
        ctk.CTkLabel(self.contenedor, text="Servicio", font=("Arial", 12)).pack(anchor="w", padx=10)
        self.combo_servicio = ctk.CTkComboBox(
            self.contenedor,
            values=["Modulo", "Vidrio", "Pin de carga", "Revisión", "Otros"]
        )

        self.combo_servicio.set("Seleccionar servicio")
        self.combo_servicio.pack(pady=5, padx=10, fill="x")

        self.entry_marca = ctk.CTkEntry(self.contenedor, placeholder_text="Marca", state="readonly")
        self.entry_marca.pack(pady=5, padx=10, fill="x")

        self.entry_modelo = ctk.CTkEntry(self.contenedor, placeholder_text="Modelo", state="readonly")
        self.entry_modelo.pack(pady=5, padx=10, fill="x")

        self.entry_contrasena = ctk.CTkEntry(self.contenedor, placeholder_text="Contraseña", state="readonly")
        self.entry_contrasena.pack(pady=5, padx=10, fill="x")

        self.entry_problema = ctk.CTkEntry(self.contenedor, placeholder_text="Problema", state="readonly")
        self.entry_problema.pack(pady=5, padx=10, fill="x")

        self.entry_presupuesto = ctk.CTkEntry(self.contenedor, placeholder_text="Presupuesto", state="readonly")
        self.entry_presupuesto.pack(pady=5, padx=10, fill="x")

        self.entry_sena = ctk.CTkEntry(self.contenedor, placeholder_text="Seña", state="readonly")
        self.entry_sena.pack(pady=5, padx=10, fill="x")

        self.entry_garantia = ctk.CTkEntry(self.contenedor, placeholder_text="Garantía", state="readonly")
        self.entry_garantia.pack(pady=5, padx=10, fill="x")

        self.entry_fecha_reparacion = ctk.CTkEntry(self.contenedor, placeholder_text="Fecha de reparación", state="readonly")
        self.entry_fecha_reparacion.pack(pady=5, padx=10, fill="x")

        self.entry_fecha_retiro = ctk.CTkEntry(self.contenedor, placeholder_text="Fecha de retiro", state="readonly")
        self.entry_fecha_retiro.pack(pady=5, padx=10, fill="x")

        self.entry_comentario_tecnico = ctk.CTkEntry(self.contenedor, placeholder_text="Comentario técnico", state="readonly")
        self.entry_comentario_tecnico.pack(pady=5, padx=10, fill="x")

        # Botones
        btn_frame = ctk.CTkFrame(self.contenedor, fg_color="transparent")
        btn_frame.pack(pady=20)

        ctk.CTkButton(btn_frame, text="Guardar", command=self.guardar_turno).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="Cancelar", fg_color="gray", command=self.destroy).pack(side="left", padx=10)

        # Datos internos
        self.cliente_data = None

    def actualizar_fecha_seleccionada(self, fecha: datetime):
        """Recibe un objeto datetime del ModernCalendar"""
        self.fecha_seleccionada = fecha.strftime("%d/%m/%Y")
        print("Fecha guardada:", self.fecha_seleccionada)
        
    def buscar_cliente(self):
        dni_str = self.entry_dni.get().strip()
        if not dni_str:
            messagebox.showwarning("Campo vacío", "Por favor ingresa un DNI")
            return

        try:
            dni = int(dni_str)
        except ValueError:
            messagebox.showerror("Error", "El DNI debe ser un número válido")
            return

        try:
            res = supabase.table("clientes").select("*").eq("dni", dni).execute()
            if res.data:
                cliente = res.data[0]
                self.cliente_data = cliente
                self.label_nombre.configure(text=f"Nombre: {cliente['numeroOrden']}")
                self.label_telefono.configure(text=f"Teléfono: {cliente.get('telefono', 'No registrado')}")
                self.label_email.configure(text=f"Email: {cliente.get('email', 'No registrado')}")

                # Llenar otros campos del cliente
                self.entry_marca.insert(0, cliente.get("marca", ""))
                self.entry_modelo.insert(0, cliente.get("modelo", ""))
                self.entry_contrasena.insert(0, cliente.get("contrasena", ""))
                self.entry_problema.insert(0, cliente.get("problema", ""))
                self.entry_presupuesto.insert(0, str(cliente.get("presupuesto", "")))
                self.entry_sena.insert(0, str(cliente.get("sena", "")))
                self.entry_garantia.insert(0, str(cliente.get("garantia", "")))
                self.entry_fecha_reparacion.insert(0, cliente.get("fechaReparacion", ""))
                self.entry_fecha_retiro.insert(0, cliente.get("fechaRetiro", ""))
                self.entry_comentario_tecnico.insert(0, cliente.get("comentarioTec", ""))
            else:
                self.limpiar_datos_cliente()
                messagebox.showinfo("Cliente no encontrado", "No se encontró un cliente con ese DNI")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo buscar el cliente: {e}")

    def limpiar_datos_cliente(self):
        self.cliente_data = None
        self.label_nombre.configure(text="")
        self.label_telefono.configure(text="")
        self.label_email.configure(text="")
        # Limpiar otros campos relacionados con el cliente
        self.entry_marca.delete(0, ctk.END)
        self.entry_modelo.delete(0, ctk.END)
        self.entry_contrasena.delete(0, ctk.END)
        self.entry_problema.delete(0, ctk.END)
        self.entry_presupuesto.delete(0, ctk.END)
        self.entry_sena.delete(0, ctk.END)
        self.entry_garantia.delete(0, ctk.END)
        self.entry_fecha_reparacion.delete(0, ctk.END)
        self.entry_fecha_retiro.delete(0, ctk.END)
        self.entry_comentario_tecnico.delete(0, ctk.END)

    def validar_campos_obligatorios(self):
        required_fields = {
        "DNI": self.entry_dni.get().strip(),
        "Servicio": self.combo_servicio.get(),
        "Fecha": self.fecha_seleccionada,
        "Presupuesto": self.entry_presupuesto.get().strip(),
        "Seña": self.entry_sena.get().strip(),
        "Fecha Reparación": self.fecha_reparacion.get().strip(),
        "Fecha Retiro": self.fecha_retiro.get().strip(),
    }
        for nombre_campo, valor in required_fields.items():
            if not valor:
                messagebox.showwarning("Campos vacíos", f"El campo '{nombre_campo}' es obligatorio.")
                return False

        return True

    def guardar_turno(self):
        dni = self.entry_dni.get()
        hora = self.entry_hora.get()
        servicio = self.combo_servicio.get()

        if not self.cliente_data:
            messagebox.showwarning("Cliente no encontrado", "Debes buscar un cliente antes de guardar")
            return

        if not self.validar_campos_obligatorios():
            return

        try:
            # Datos del cliente
            cliente = self.cliente_data
            dni = cliente["dni"]
            nombre_cliente = cliente["nombre"]

            # Datos del turno
            hora = self.entry_hora.get().strip()
            servicio = self.combo_servicio.get()
            presupuesto = float(self.entry_presupuesto.get().strip())
            sena = float(self.entry_sena.get().strip())
            garantia = self.garantia_var.get()
            fecha_reparacion = self.fecha_reparacion.get().strip()
            fecha_retiro = self.fecha_retiro.get().strip()
            comentario_tec = self.comentario_tecnico.get().strip()

            datos = {
                "cliente_id": cliente["id"],
                "cliente": nombre_cliente,
                "dni": dni,
                "servicio": servicio,
                "presupuesto": presupuesto,
                "sena": sena,
                "garantia": garantia,
                "fechaReparacion": fecha_reparacion,
                "fechaRetiro": fecha_retiro,
                "comentarioTec": comentario_tec,
            }

            from config.supabase_client import insertar_con_respaldo
            insertar_con_respaldo("Telefonos", datos)
            messagebox.showinfo("Éxito", "Turno guardado correctamente")
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el turno: {e}")