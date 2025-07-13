import customtkinter as ctk
from tkinter import messagebox
from utils.session_manager import guardar_sesion, cargar_sesion
from utils.credentials_manager import CredentialsManager
import utils.util_ventana as util_ventana
from PIL import Image

# Importamos nuestras funciones personalizadas de Supabase
from config.supabase_client import login as supabase_login
from config.supabase_client import signup as supabase_signup


class AuthApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Login")
        w, h = 900, 700
        util_ventana.centrar_ventana(self, w, h)
        self.resizable(False, False)
        ctk.set_appearance_mode("dark")

        self.title_font = ctk.CTkFont(family="Century Gothic", size=20, weight="bold")
        self.label_font = ctk.CTkFont(family="Banshcrift", size=12)
        self.button_font = ctk.CTkFont(family="Century Gothic", size=12, weight="bold")

        self.bg_image = ctk.CTkImage(Image.open("assets/background.png"), size=(w, h))
        # Fondo como label
        self.background_label = ctk.CTkLabel(self, image=self.bg_image, text="")
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Estado del login
        self.usuario_autenticado = False
        self.session_data = cargar_sesion()

        # Contenedor
        self.contenedor = ctk.CTkFrame(self, corner_radius=32, fg_color="transparent")
        self.contenedor.pack(pady=150, padx=300, fill="both", expand=True)
        
        self.mostrar_login()

    def limpiar_contenedor(self):
        for widget in self.contenedor.winfo_children():
            widget.destroy()
    
    def mostrar_login(self):
        self.limpiar_contenedor()
        ctk.CTkLabel(self.contenedor, text="Inicia Sesión en tu Cuenta", font=self.title_font).pack(pady=20)

        #!!Campo email
        self.entry_email = ctk.CTkEntry(self.contenedor, placeholder_text="Email")
        self.entry_email.pack(pady=10, fill="x", padx=40)

        #!!Campo contraseña
        self.entry_pass = ctk.CTkEntry(self.contenedor, placeholder_text="Contraseña", show="*")
        self.entry_pass.pack(pady=10, fill="x", padx=40)

        if self.session_data and "password" in self.session_data:
            self.entry_email.insert(0, self.session_data["email"])
            self.entry_pass.insert(0, self.session_data["password"])

        self.mostrar_pass_var = ctk.BooleanVar()
        self.check_mostrar = ctk.CTkCheckBox(
            self.contenedor,
            text="Mostrar Contraseña",
            variable=self.mostrar_pass_var,
            command=self.toggle_mostrar_contrasena,
            corner_radius=32,
            border_width=2, checkbox_height=10, checkbox_width=10, font=self.label_font
        )
        self.check_mostrar.pack(pady=5, padx=40, fill="x")

        self.recordar_var = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(
            self.contenedor,
            text="Recordar sesión",
            variable=self.recordar_var,
            corner_radius=32,
            border_width=2, checkbox_height=10, checkbox_width=10, font=self.label_font
        ).pack(pady=5, padx=40, fill="x")
        
        ctk.CTkButton(self.contenedor, text="Entrar", command=self._intentar_login, border_color="#0081AF", border_width=2, fg_color="transparent").pack(pady=10, padx=40, fill="x")
        ctk.CTkButton(self.contenedor, text="¿Olvidaste tu contraseña?", fg_color="transparent", font=self.button_font,
                      command=self.mostrar_recuperar).pack(pady=5, padx=40, fill="x")
        ctk.CTkButton(self.contenedor, text="Crear Cuenta", fg_color="transparent", font=self.button_font,
                      command=self.mostrar_signup).pack(pady=5, padx=40, fill="x")
        
        if self.session_data:
            ctk.CTkButton(
                self.contenedor,
                text="Cerrar Sesión",
                fg_color="transparent",
                hover_color="dark red",
                font=self.button_font,
                command=self.cerrar_sesion
            ).pack(pady=(0, 10))

    def toggle_mostrar_contrasena(self):
        if self.mostrar_pass_var.get():
            self.entry_pass.configure(show="")
        else:
            self.entry_pass.configure(show="*")
    
    def cerrar_sesion(self):
        from utils.session_manager import cerrar_sesion
        cerrar_sesion()
        self.session_data = None
        self.mostrar_login()

    def mostrar_signup(self):
        self.limpiar_contenedor()
        ctk.CTkLabel(self.contenedor, text="Crear Cuenta", font=("Arial", 20)).pack(pady=20)

        self.entry_email_signup = ctk.CTkEntry(self.contenedor, placeholder_text="Email")
        self.entry_email_signup.pack(pady=10, fill="x", padx=40)

        self.entry_pass_signup = ctk.CTkEntry(self.contenedor, placeholder_text="Contraseña", show="*")
        self.entry_pass_signup.pack(pady=10, fill="x", padx=40)

        self.entry_pass_confirm = ctk.CTkEntry(self.contenedor, placeholder_text="Confirmar Contraseña", show="*")
        self.entry_pass_confirm.pack(pady=10, fill="x", padx=40)

        ctk.CTkButton(self.contenedor, text="Registrar", command=self.signup).pack(pady=10)
        ctk.CTkButton(self.contenedor, text="Volver al Inicio de Sesión", fg_color="transparent",
                      hover=False, command=self.mostrar_login).pack(pady=5)

    def mostrar_recuperar(self):
        self.limpiar_contenedor()
        ctk.CTkLabel(self.contenedor, text="Recuperar Contraseña", font=("Arial", 20)).pack(pady=20)

        self.entry_email_recuperar = ctk.CTkEntry(self.contenedor, placeholder_text="Email")
        self.entry_email_recuperar.pack(pady=10)

        ctk.CTkButton(self.contenedor, text="Enviar Instrucciones", command=self.recuperar).pack(pady=10)
        ctk.CTkButton(self.contenedor, text="Volver al Inicio de Sesión", fg_color="transparent",
                      hover=False, command=self.mostrar_login).pack(pady=5)

    def _intentar_login(self):
        email = self.entry_email.get()
        password = self.entry_pass.get()

        if not email or not password:
            messagebox.showwarning("Campos vacíos", "Por favor completa todos los campos")
            return

        try:
            res = supabase_login(email, password)
            if res.user:
                if self.recordar_var.get():
                    CredentialsManager().save_credentials(email, password)
                else:
                    CredentialsManager().clear_credentials()
                self.usuario_autenticado = True
                self.withdraw()
                self.update()
                self.destroy()
            else:
                messagebox.showerror("Error", "Credenciales incorrectas")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo iniciar sesión: {e}")

    def signup(self):
        email = self.entry_email_signup.get()
        pass1 = self.entry_pass_signup.get()
        pass2 = self.entry_pass_confirm.get()

        if not email or not pass1 or not pass2:
            messagebox.showwarning("Error", "Todos los campos son obligatorios")
            return

        if pass1 != pass2:
            messagebox.showerror("Error", "Las contraseñas no coinciden")
            return

        try:
            response = supabase_signup(email, pass1)
            if response.user:
                messagebox.showinfo("Éxito", "Usuario creado exitosamente. Revisa tu correo para confirmarlo.")
                self.mostrar_login()
            else:
                messagebox.showerror("Error", "No se pudo crear el usuario")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar: {e}")

    def recuperar(self):
        email = self.entry_email_recuperar.get()
        if not email:
            messagebox.showwarning("Error", "Ingresa tu correo electrónico")
            return

        try:
            messagebox.showinfo("Instrucciones", f"Se ha enviado un enlace de recuperación a {email}.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo procesar la solicitud: {e}")