import customtkinter as ctk
from tkcalendar import Calendar
from datetime import datetime, date
from typing import Dict, List
from models.turno import Turno
from services.turno_service import TurnoService

class TurnoDialog(ctk.CTkToplevel):
    def __init__(self, parent=None, turno: Turno = None):
        super().__init__(parent)
        self.turno = turno or Turno()
        self.result = None
        self.setup_ui()
        
        # Hacer la ventana modal
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.reject)
        
        # Centrar la ventana
        self.center_window()

    def setup_ui(self):
        self.title("Turno")
        self.geometry("400x600")

        # Contenedor principal
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # Campos del formulario
        self.nombre_label = ctk.CTkLabel(
            main_frame, 
            text="Nombre:",
            font=("Helvetica", 14)
        )
        self.nombre_label.pack(pady=(10,5))
        
        self.nombre_input = ctk.CTkEntry(
            main_frame,
            width=300,
            placeholder_text="Nombre del cliente"
        )
        self.nombre_input.insert(0, self.turno.nombre)
        self.nombre_input.pack()

        self.fecha_label = ctk.CTkLabel(
            main_frame,
            text="Fecha y Hora:",
            font=("Helvetica", 14)
        )
        self.fecha_label.pack(pady=(20,5))
        
        # Frame para fecha y hora
        time_frame = ctk.CTkFrame(main_frame)
        time_frame.pack(pady=5)
        
        # Calendario
        self.calendario = Calendar(
            time_frame,
            selectmode='day',
            date_pattern='dd/mm/yyyy'
        )
        self.calendario.pack(pady=5)
        
        # Frame para hora y minutos
        hora_frame = ctk.CTkFrame(time_frame)
        hora_frame.pack(pady=10)
        
        # Selector de hora
        self.hora_spin = ctk.CTkOptionMenu(
            hora_frame,
            values=[f"{i:02d}" for i in range(24)]
        )
        self.hora_spin.pack(side="left", padx=5)
        
        # Separador
        ctk.CTkLabel(hora_frame, text=":").pack(side="left")
        
        # Selector de minutos
        self.min_spin = ctk.CTkOptionMenu(
            hora_frame,
            values=[f"{i:02d}" for i in range(0, 60, 15)]
        )
        self.min_spin.pack(side="left", padx=5)
        
        # Establecer fecha y hora actual
        self.calendario.selection_set(self.turno.fecha_hora.date())
        self.hora_spin.set(f"{self.turno.fecha_hora.hour:02d}")
        self.min_spin.set(f"{self.turno.fecha_hora.minute:02d}")

        # Checkbox confirmado
        self.confirmado_check = ctk.CTkCheckBox(
            main_frame, 
            text="Confirmado",
            font=("Helvetica", 12),
            checkbox_height=25,
            checkbox_width=25
        )
        if self.turno.confirmado:
            self.confirmado_check.select()
        self.confirmado_check.pack(pady=20)

        # Botones
        button_frame = ctk.CTkFrame(main_frame)
        button_frame.pack(pady=20, fill="x")
        
        self.btn_guardar = ctk.CTkButton(
            button_frame,
            text="Guardar",
            command=self.accept,
            width=120,
            height=35,
            font=("Helvetica", 14)
        )
        self.btn_guardar.pack(side="left", padx=10, expand=True)
        
        self.btn_cancelar = ctk.CTkButton(
            button_frame,
            text="Cancelar",
            command=self.reject,
            width=120,
            height=35,
            font=("Helvetica", 14),
            fg_color="gray"
        )
        self.btn_cancelar.pack(side="left", padx=10, expand=True)

    def center_window(self):
        """Centra la ventana en la pantalla"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def accept(self):
        self.result = True
        self.destroy()

    def reject(self):
        self.result = False
        self.destroy()

    def get_turno(self) -> Turno:
        """Retorna el turno con los datos del formulario"""
        self.turno.nombre = self.nombre_input.get()
        fecha = datetime.strptime(self.calendario.get_date(), '%d/%m/%Y').date()
        hora = int(self.hora_spin.get())
        minuto = int(self.min_spin.get())
        self.turno.fecha_hora = datetime.combine(
            fecha,
            datetime.min.time().replace(hour=hora, minute=minuto)
        )
        self.turno.confirmado = bool(self.confirmado_check.get())
        return self.turno


class CalendarioView(ctk.CTk):
    def __init__(self, turno_service: TurnoService):
        super().__init__()
        self.turno_service = turno_service
        self.setup_ui()
        self.setup_refresh_timer()
        self.cargar_turnos()

    def setup_ui(self):
        self.title("Gestor de Turnos")
        self.geometry("1200x800")

        # Crear menú superior con botón de logout
        self.menu_frame = ctk.CTkFrame(self, height=40)
        self.menu_frame.pack(fill="x", pady=5, padx=5)
        
        self.logout_button = ctk.CTkButton(
            self.menu_frame,
            text="Cerrar Sesión",
            command=self.handle_logout,
            width=100
        )
        self.logout_button.pack(side="right", padx=10)

        # Contenedor principal
        main_container = ctk.CTkFrame(self)
        main_container.pack(expand=True, fill="both", padx=10, pady=5)
        
        # Configurar grid del contenedor principal
        main_container.grid_columnconfigure(0, weight=1)
        main_container.grid_columnconfigure(1, weight=2)
        main_container.grid_rowconfigure(0, weight=1)

        # Panel izquierdo
        left_panel = ctk.CTkFrame(main_container)
        left_panel.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # Calendario
        self.calendario = Calendar(
            left_panel,
            selectmode='day',
            date_pattern='dd/mm/yyyy'
        )
        self.calendario.pack(pady=10, padx=10, fill="x")
        self.calendario.bind("<<CalendarSelected>>", self.on_fecha_seleccionada)

        # Botón nuevo turno
        self.btn_nuevo = ctk.CTkButton(
            left_panel,
            text="Nuevo Turno",
            command=self.mostrar_dialogo_nuevo_turno
        )
        self.btn_nuevo.pack(pady=10, padx=10, fill="x")

        # Panel derecho (lista de turnos)
        right_panel = ctk.CTkFrame(main_container)
        right_panel.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        
        # Lista de turnos
        self.lista_turnos = ctk.CTkScrollableFrame(right_panel)
        self.lista_turnos.pack(expand=True, fill="both", padx=10, pady=10)

    def handle_logout(self):
        """Maneja el cierre de sesión"""
        try:
            from config.supabase_client import logout
            logout()
            self.quit()  # Cerrar la aplicación
        except Exception as e:
            self.mostrar_error("Error", f"Error al cerrar sesión: {str(e)}")

    def mostrar_error(self, titulo: str, mensaje: str):
        """Muestra un diálogo de error"""
        dialog = ctk.CTkInputDialog(
            text=mensaje,
            title=titulo
        )
        dialog.get_input()

    def actualizar_lista_turnos(self, turnos: List[Turno]):
        """Actualiza la lista de turnos en la UI"""
        # Limpiar lista actual
        for widget in self.lista_turnos.winfo_children():
            widget.destroy()

        # Agregar turnos
        for turno in turnos:
            turno_frame = ctk.CTkFrame(self.lista_turnos)
            turno_frame.pack(fill="x", pady=5, padx=5)

            texto = f"{turno.fecha_hora.strftime('%H:%M')} - {turno.nombre}"
            if turno.confirmado:
                texto += " ✓"

            label = ctk.CTkLabel(
                turno_frame,
                text=texto,
                anchor="w"
            )
            label.pack(side="left", padx=10)

            # Botones de acción
            btn_editar = ctk.CTkButton(
                turno_frame,
                text="Editar",
                command=lambda t=turno: self.editar_turno(t),
                width=80
            )
            btn_editar.pack(side="right", padx=5)

            btn_eliminar = ctk.CTkButton(
                turno_frame,
                text="Eliminar",
                command=lambda t=turno: self.eliminar_turno(t),
                fg_color="red",
                width=80
            )
            btn_eliminar.pack(side="right", padx=5)

            if not turno.confirmado:
                btn_confirmar = ctk.CTkButton(
                    turno_frame,
                    text="Confirmar",
                    command=lambda t=turno: self.confirmar_turno(t),
                    fg_color="green",
                    width=80
                )
                btn_confirmar.pack(side="right", padx=5)

    def setup_refresh_timer(self):
        """Configura un timer para actualizar los turnos cada 30 segundos"""
        self.after(30000, self.cargar_turnos)

    def mostrar_dialogo_nuevo_turno(self):
        """Muestra el diálogo para crear un nuevo turno"""
        fecha_seleccionada = datetime.strptime(
            self.calendario.get_date(),
            '%d/%m/%Y'
        ).date()
        
        turno = Turno()
        turno.fecha_hora = datetime.combine(
            fecha_seleccionada,
            datetime.now().time()
        )
        
        dialogo = TurnoDialog(self, turno)
        self.wait_window(dialogo)
        
        if dialogo.result:
            try:
                nuevo_turno = dialogo.get_turno()
                self.turno_service.agendar_turno(nuevo_turno)
                self.cargar_turnos()
            except Exception as e:
                self.mostrar_error("Error al guardar turno", str(e))

    def editar_turno(self, turno: Turno):
        """Muestra el diálogo para editar un turno"""
        dialogo = TurnoDialog(self, turno)
        self.wait_window(dialogo)
        
        if dialogo.result:
            try:
                turno_actualizado = dialogo.get_turno()
                self.turno_service.actualizar_turno(turno_actualizado)
                self.cargar_turnos()
            except Exception as e:
                self.mostrar_error("Error al editar turno", str(e))

    def confirmar_turno(self, turno: Turno):
        """Confirma un turno"""
        try:
            self.turno_service.confirmar_turno(turno.id)
            self.cargar_turnos()
        except Exception as e:
            self.mostrar_error("Error", str(e))

    def eliminar_turno(self, turno: Turno):
        """Elimina un turno"""
        if self.confirmar_eliminar():
            try:
                self.turno_service.eliminar_turno(turno.id)
                self.cargar_turnos()
            except Exception as e:
                self.mostrar_error("Error", str(e))

    def confirmar_eliminar(self) -> bool:
        """Muestra diálogo de confirmación para eliminar"""
        dialog = ctk.CTkInputDialog(
            text="¿Está seguro que desea eliminar este turno?\nEscriba 'SI' para confirmar",
            title="Confirmar eliminación"
        )
        result = dialog.get_input()
        return result == "SI"

    def cargar_turnos(self):
        """Carga los turnos del día seleccionado"""
        try:
            fecha = datetime.strptime(
                self.calendario.get_date(),
                '%d/%m/%Y'
            ).date()
            turnos = self.turno_service.obtener_turnos_por_fecha(fecha)
            self.actualizar_lista_turnos(turnos)
        except Exception as e:
            self.mostrar_error("Error al cargar turnos", str(e))

    def on_fecha_seleccionada(self):
        """Maneja el cambio de fecha seleccionada"""
        self.cargar_turnos() 