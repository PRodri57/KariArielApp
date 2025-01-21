import customtkinter as ctk
from tkcalendar import Calendar
from datetime import datetime, date
from models.turno import Turno

class TurnoDialog(ctk.CTkToplevel):
    def __init__(self, parent=None, turno: Turno = None):
        super().__init__(parent)
        self.turno = turno or Turno()
        self.result = None
        
        # Hacer la ventana modal y esperar a que esté lista
        self.wait_visibility()
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.reject)
        
        # Configurar UI después de que la ventana esté lista
        self.setup_ui()
        self.center_window()

    def setup_ui(self):
        self.title("Turno")
        self.geometry("500x700")
        self.minsize(500, 700)

        # Contenedor principal con padding
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(expand=True, fill="both", padx=30, pady=30)

        # Campos del formulario
        self.nombre_label = ctk.CTkLabel(
            main_frame, 
            text="Nombre:",
            font=("Helvetica", 14)
        )
        self.nombre_label.pack(pady=(10,5))
        
        self.nombre_input = ctk.CTkEntry(
            main_frame,
            width=400,
            height=35,
            placeholder_text="Nombre del cliente",
            font=("Helvetica", 14)
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
        """Acepta el diálogo y limpia los widgets"""
        self.result = True
        # Desactivar widgets antes de destruir
        for widget in self.winfo_children():
            if isinstance(widget, (ctk.CTkButton, ctk.CTkEntry, ctk.CTkCheckBox)):
                widget.configure(state="disabled")
        # Esperar a que terminen las animaciones
        self.after(100, self._destroy)

    def reject(self):
        """Rechaza el diálogo y limpia los widgets"""
        self.result = False
        # Desactivar widgets antes de destruir
        for widget in self.winfo_children():
            if isinstance(widget, (ctk.CTkButton, ctk.CTkEntry, ctk.CTkCheckBox)):
                widget.configure(state="disabled")
        # Esperar a que terminen las animaciones
        self.after(100, self._destroy)

    def _destroy(self):
        """Método seguro para destruir la ventana"""
        try:
            # Liberar el grab antes de destruir
            self.grab_release()
            # Destruir la ventana
            self.destroy()
        except Exception:
            pass

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

