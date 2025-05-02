import customtkinter as ctk
from PIL import Image

class HomeFrame(ctk.CTkFrame):
    def __init__(self, parent, on_enter):
        super().__init__(parent)
        logo = ctk.CTkImage(Image.open("assets/icono.png"), size=(300, 300))
        self.logo_label = ctk.CTkLabel(self, text="Bienvenido/a a KariAriel", image=logo,
                                       fg_color="transparent", font=("Bahnschrift", 40, "bold"), compound="top")
        self.logo_label.pack(pady=20, padx=20, anchor="center")
