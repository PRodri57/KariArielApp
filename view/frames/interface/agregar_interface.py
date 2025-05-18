import customtkinter as ctk
import utils.util_ventana as utils_ventana
from abc import ABC, abstractmethod
from tkinter import messagebox

class BaseDialog(ctk.CTkToplevel, ABC):
    """
    Clase base abstracta para diálogos modales en CustomTkinter.
    Proporciona una estructura común para la creación de formularios y botones de acción.
    """
    def __init__(self, parent, title: str, width: int, height: int):
        super().__init__(parent)

        self.parent_window = parent
        self.title(title)
        w, h = 700, 700
        utils_ventana.centrar_ventana(self, w, h)
        self.transient(parent)  # Mantener el diálogo sobre la ventana padre
        self.grab_set()         # Hacer el diálogo modal (bloquea la interacción con la ventana padre)

        # Contenedor principal para todo el contenido
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(pady=20, padx=30, fill="both", expand=True)

        # Frame para los widgets del formulario (contenido específico del diálogo)
        self.form_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.form_frame.pack(pady=(0, 20), padx=0, fill="both", expand=True)
        self._create_form_widgets(self.form_frame) # Llamada al método abstracto

        # Frame para los botones de acción
        self.buttons_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.buttons_frame.pack(pady=(10, 0), fill="x", side="bottom") # Empaquetar abajo
        self._create_action_buttons(self.buttons_frame) # Llamada al método para crear botones

        self.result = None # Para almacenar el resultado del diálogo si es necesario

    @abstractmethod
    def _create_form_widgets(self, master_frame: ctk.CTkFrame):
        """
        Las subclases DEBEN implementar este método para crear y empaquetar
        sus widgets específicos dentro del 'master_frame' proporcionado.
        """
        self.entry_dni = ctk.CTkEntry(master_frame, placeholder_text="DNI")
        self.entry_dni.pack(pady=(0, 10), padx=0, fill="x")
        self.entry_dni.bind("<KeyRelease>", self.buscar_cliente_auto)

    def _create_action_buttons(self, master_frame: ctk.CTkFrame):
        """
        Crea los botones de acción estándar "Guardar" y "Cancelar".
        Las subclases pueden sobrescribir este método si necesitan botones diferentes
        o una disposición distinta.
        """
        self.save_button = ctk.CTkButton(master_frame, text="Guardar", command=self._on_save_pressed, width=120)
        self.save_button.pack(side="right", padx=(10,0)) # Alinear a la derecha

        self.cancel_button = ctk.CTkButton(master_frame, text="Cancelar", command=self.destroy, fg_color="gray", width=120)
        self.cancel_button.pack(side="right", padx=(0,10)) # Alinear a la derecha, antes de guardar


    def _on_save_pressed(self):
        """
        Se llama cuando se presiona el botón "Guardar".
        Primero valida el formulario y luego ejecuta la acción de guardado.
        """
        if self._validate_form():
            self._perform_save_action()
        # No es necesario un 'else' aquí si _validate_form muestra sus propios mensajes.

    @abstractmethod
    def _validate_form(self) -> bool:
        """
        Las subclases DEBEN implementar este método para validar los datos del formulario.
        Debe devolver True si la validación es exitosa, False en caso contrario.
        Es responsabilidad de este método mostrar mensajes de error/advertencia.
        """
        pass

    @abstractmethod
    def _perform_save_action(self):
        """
        Las subclases DEBEN implementar este método para definir qué sucede
        cuando se presiona "Guardar" y la validación ha sido exitosa
        (por ejemplo, guardar datos en una base de datos, actualizar la UI principal, etc.).
        """
        pass

    def get_result(self):
        """
        Permite recuperar datos del diálogo después de que se cierra,
        si _perform_save_action establece self.result.
        """
        return self.result

    def run_dialog(self):
        """
        Hace que el diálogo se ejecute y espere hasta que se cierre.
        Útil si la ventana padre necesita esperar a que el diálogo termine.
        """
        self.wait_window()
        return self.get_result()