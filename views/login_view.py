import customtkinter as ctk
import tkinter as tk
from config.supabase_client import login, signup
from utils.credentials_manager import CredentialsManager
from tkinter import *
from tkinter import messagebox

class LoginDialog(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.result = False
        self.credentials_manager = CredentialsManager()
        self.setup_ui()
        self.load_saved_credentials()
        
    def setup_ui(self):
        # Configuración de la ventana
        self.title("Iniciar Sesión")
        self.minsize(400, 500)
        self.geometry("1000x1200")
        
        # Contenedor principal
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # Título
        title_label = ctk.CTkLabel(
            main_frame,
            text="Bienvenido a KariAriel",
            font=("Helvetica", 16)
        )
        title_label.pack(pady=20)

        # Campos de login
        self.email_label = ctk.CTkLabel(main_frame,text="Email:",font=("Helvetica", 14))
        self.email_label.pack(pady=(20,5))
        
        self.email_input = ctk.CTkEntry(main_frame,width=300,placeholder_text="ejemplo@email.com")
        self.email_input.pack()

        self.password_label = ctk.CTkLabel(main_frame,text="Contraseña:",font=("Helvetica", 14))
        self.password_label.pack(pady=(20,5))
        
        self.password_input = ctk.CTkEntry(main_frame,width=300,show="*",placeholder_text="Ingrese su contraseña", corner_radius=10)
        self.password_input.pack()

        self.checkbox = ctk.CTkCheckBox(main_frame, text="Recordar usuario")
        self.checkbox.pack(pady=12, padx=10)

        # Botones
        button_frame = ctk.CTkFrame(main_frame)
        button_frame.pack(pady=30)
        
        self.login_button = ctk.CTkButton(button_frame,text="Iniciar Sesión",command=self.handle_login,width=140,height=40,font=("Helvetica", 14))
        self.login_button.pack(side="left", padx=10)
        
        self.signup_button = ctk.CTkButton(button_frame,text="Registrarse",command=self.handle_signup,width=140,height=40,font=("Helvetica", 14),fg_color="gray")
        self.signup_button.pack(side="left", padx=10)

        # Centrar la ventana
        self.center_window()
        
        # Hacer la ventana modal
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def center_window(self):
        """Centra la ventana en la pantalla"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 1)
        y = (self.winfo_screenheight() // 2) - (height // 1)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def load_saved_credentials(self):
        """Carga credenciales guardadas si existen"""
        credentials = self.credentials_manager.load_credentials()
        if credentials:
            self.email_input.insert(0, credentials['email'])
            self.password_input.insert(0, credentials['password'])
            self.checkbox.select()  # Marcar checkbox

    def handle_login(self):
        """Maneja el inicio de sesión"""
        try:
            email = self.email_input.get()
            password = self.password_input.get()
            
            if not email or not password:
                self.mostrar_error(
                    "Error",
                    "Por favor, complete todos los campos"
                )
                return
                
            response = login(email, password)
            
            if response and hasattr(response, 'user') and response.user:
                if self.checkbox.get():
                    self.credentials_manager.save_credentials(email, password)
                else:
                    self.credentials_manager.clear_credentials()
                    
                self.result = True
                self.destroy()
            else:
                self.mostrar_error(
                    "Error",
                    "Email o contraseña incorrectos"
                )
        except Exception as e:
            print(f"Error de login: {str(e)}")
            self.mostrar_error(
                "Error",
                f"Error al iniciar sesión: {str(e)}"
            )

    def handle_signup(self):
        """Maneja el registro de usuario"""
        try:
            response = signup(
                self.email_input.get(),
                self.password_input.get()
            )
            if response.user:
                self.mostrar_info(
                    "Éxito",
                    "Usuario registrado correctamente.\nPor favor, verifica tu email."
                )
            else:
                self.mostrar_error(
                    "Error",
                    "No se pudo crear el usuario"
                )
        except Exception as e:
            self.mostrar_error(
                "Error",
                f"Error al registrar: {str(e)}"
            )

    def mostrar_error(self, titulo: str, mensaje: str):
        """Muestra un diálogo de error"""
        #dialog = tk.TkDialog(master=self, title=titulo, text=mensaje, cancel_button=False)
        dialog = messagebox.showerror("Error", "Intenta de nuevo")
        #dialog.wait_event()

    def mostrar_info(self, titulo: str, mensaje: str):
        """Muestra un diálogo informativo"""
        #dialog = tk.TkDialog(master=self, title=titulo, text=mensaje, cancel_button=False)
        dialog = messagebox.showerror("Info", "...")
        #dialog.wait_event()

    def on_closing(self):
        """Maneja el cierre de la ventana"""
        self.result = False
        self.destroy() 