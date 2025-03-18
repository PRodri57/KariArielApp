import customtkinter as ctk
from tkinter import messagebox
from config.supabase_client import login, signup
from utils.credentials_manager import CredentialsManager

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
        self.geometry("600x600")  # Dimensiones más razonables
        
        # Contenedor principal
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # Título
        title_label = ctk.CTkLabel(
            self.main_frame,
            text="Bienvenido a KariAriel",
            font=("Helvetica", 24)  # Tamaño de fuente más grande
        )
        title_label.pack(pady=20)

        # Campos de login
        self.create_form_field("Email:", "ejemplo@email.com", is_password=False)
        self.create_form_field("Contraseña:", "Ingrese su contraseña", is_password=True)

        self.checkbox = ctk.CTkCheckBox(self.main_frame, text="Recordar usuario")
        self.checkbox.pack(pady=12)

        # Botones
        button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        button_frame.pack(pady=30)
        
        self.login_button = self.create_button(
            button_frame, "Iniciar Sesión", self.handle_login, primary=True
        )
        self.login_button.pack(side="left", padx=10)
        
        self.signup_button = self.create_button(
            button_frame, "Registrarse", self.handle_signup, primary=False
        )
        self.signup_button.pack(side="left", padx=10)

        # Centrar la ventana
        self.center_window()
        
        # Hacer la ventana modal
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_form_field(self, label_text, placeholder, is_password=False):
        """Crea un campo de formulario con etiqueta y entrada"""
        label = ctk.CTkLabel(
            self.main_frame,
            text=label_text,
            font=("Helvetica", 14)
        )
        label.pack(pady=(20, 5), anchor="w", padx=50)
        
        entry = ctk.CTkEntry(
            self.main_frame,
            width=300,
            placeholder_text=placeholder,
            show="*" if is_password else "",
            corner_radius=10
        )
        entry.pack(pady=(0, 10))
        
        # Guardar referencia al campo
        if "Email" in label_text:
            self.email_input = entry
        elif "Contraseña" in label_text:
            self.password_input = entry
            
        return entry

    def create_button(self, parent, text, command, primary=True):
        """Crea un botón con estilo consistente"""
        return ctk.CTkButton(
            parent,
            text=text,
            command=command,
            width=140,
            height=40,
            font=("Helvetica", 14),
            fg_color="#1f538d" if primary else "#555555"
        )

    def center_window(self):
        """Centra la ventana en la pantalla"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)  # Corregido
        y = (self.winfo_screenheight() // 2) - (height // 2)  # Corregido
        self.geometry(f'{width}x{height}+{x}+{y}')

    def load_saved_credentials(self):
        """Carga credenciales guardadas si existen"""
        credentials = self.credentials_manager.load_credentials()
        if credentials and 'email' in credentials and 'password' in credentials:
            self.email_input.insert(0, credentials['email'])
            self.password_input.insert(0, credentials['password'])
            self.checkbox.select()

    def handle_login(self):
        """Maneja el inicio de sesión"""
        try:
            email = self.email_input.get().strip()
            password = self.password_input.get()
            
            if not email or not password:
                self.mostrar_mensaje("Error", "Por favor, complete todos los campos", "error")
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
                self.mostrar_mensaje("Error", "Email o contraseña incorrectos", "error")
        except Exception as e:
            print(f"Error de login: {str(e)}")
            self.mostrar_mensaje("Error", f"Error al iniciar sesión: {str(e)}", "error")

    def handle_signup(self):
        """Maneja el registro de usuario"""
        try:
            email = self.email_input.get().strip()
            password = self.password_input.get()
            
            if not email or not password:
                self.mostrar_mensaje("Error", "Por favor, complete todos los campos", "error")
                return
                
            if len(password) < 6:
                self.mostrar_mensaje("Error", "La contraseña debe tener al menos 6 caracteres", "error")
                return
                
            response = signup(email, password)
            if response and hasattr(response, 'user') and response.user:
                self.mostrar_mensaje(
                    "Éxito",
                    "Usuario registrado correctamente.\nPor favor, verifica tu email.",
                    "info"
                )
            else:
                self.mostrar_mensaje("Error", "No se pudo crear el usuario", "error")
        except Exception as e:
            self.mostrar_mensaje("Error", f"Error al registrar: {str(e)}", "error")

    def mostrar_mensaje(self, titulo, mensaje, tipo="info"):
        """Muestra un diálogo de mensaje según el tipo"""
        if tipo == "error":
            messagebox.showerror(titulo, mensaje)
        elif tipo == "warning":
            messagebox.showwarning(titulo, mensaje)
        else:
            messagebox.showinfo(titulo, mensaje)

    def on_closing(self):
        """Maneja el cierre de la ventana"""
        self.result = False
        self.destroy()