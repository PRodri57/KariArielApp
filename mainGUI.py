import customtkinter as ctk
from view.frames.home_frame import HomeFrame
from view.frames.turnos_frame import TurnosFrame
from view.frames.clientes_frame import ClientesFrame
from view.frames.presupuesto_frame import PresupuestoFrame
from view.components.sidebar import Sidebar
import utils.util_ventana as util_ventana


class AppPrincipal(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuración básica de la ventana
        self.title("KariAriel")
        self.iconbitmap("assets/icono.ico")
        ctk.set_appearance_mode("dark")

        w, h = 1366, 768
        util_ventana.centrar_ventana(self, w, h)

        # Layout grid
        self.grid_columnconfigure(0, weight=0)  # Sidebar
        self.grid_columnconfigure(1, weight=1)  # Contenedor
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar = Sidebar(
            master=self,
            callback_dict={
                "inicio": self.mostrar_home,
                "turnos": self.mostrar_turnos,
                "clientes": self.mostrar_clientes,
                "presupuesto": self.mostrar_presupuesto
            }
        )
        self.sidebar.grid(row=0, column=0, sticky="ns")
        self.sidebar.grid_propagate(True)

        # Contenedor principal
        self.contenedor = ctk.CTkFrame(self, fg_color="transparent")
        self.contenedor.grid(row=0, column=1, sticky="nsew")

        # Frame inicial
        self.mostrar_home()

    def _mostrar_frame(self, frame_class):
        """Muestra un frame específico en el contenedor."""
        # Limpiar contenedor
        for widget in self.contenedor.winfo_children():
            widget.destroy()

        # Crear y mostrar el nuevo frame
        if callable(frame_class):
            frame = frame_class(self.contenedor)
        else:
            frame = frame_class(self.contenedor, on_enter=self.mostrar_turnos)
        frame.pack(expand=True, fill="both")

    def mostrar_home(self):
        self._mostrar_frame(lambda master: HomeFrame(master, on_enter=self.mostrar_turnos))

    def mostrar_turnos(self):
        self._mostrar_frame(TurnosFrame)

    def mostrar_clientes(self):
        self._mostrar_frame(ClientesFrame)

    def mostrar_presupuesto(self):
        self._mostrar_frame(PresupuestoFrame)