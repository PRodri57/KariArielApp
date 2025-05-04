# run.py
from login_frame import AuthApp
from mainGUI import AppPrincipal
import customtkinter as ctk
from PIL import ImageTk, Image

if __name__ == "__main__":
    # Iniciar ventana de login
    login_window = AuthApp()
    login_window.mainloop()
    

    # Si el login fue exitoso, abrir la app principal
    if getattr(login_window, "usuario_autenticado", False):
        #login_window.destroy()  # Cerrar ventana de login
        app = AppPrincipal()
        app.mainloop()