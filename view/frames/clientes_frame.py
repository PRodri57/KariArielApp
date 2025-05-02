# view/frames/clientes_frame.py
import customtkinter as ctk

class ClientesFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        titulo = ctk.CTkLabel(self, text="Lista de clientes", font=("Bahnschrift", 40, "bold"))
        titulo.pack(pady=20)

        # Acá podés agregar una tabla o scrollable frame en el futuro
        placeholder = ctk.CTkLabel(self, text="(Aquí irán los datos de los clientes)", font=("Bahnschrift", 18))
        placeholder.pack(pady=10)
