import customtkinter as ctk
from config.supabase_client import login, signup

class LoginDialog(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.result = False
        self.setup_ui()
        
    def setup_ui(self):
        # Configuración de la ventana
        self.title("Iniciar Sesión")
        self.geometry("1000x1200")
        
        # Contenedor principal
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # Título
        title_label = ctk.CTkLabel(
            main_frame,
            text="Bienvenido",
            font=("Helvetica", 16)
        )
        title_label.pack(pady=20)

        # Campos de login
        self.email_label = ctk.CTkLabel(
            main_frame,
            text="Email:",
            font=("Helvetica", 14)
        )
        self.email_label.pack(pady=(20,5))
        
        self.email_input = ctk.CTkEntry(
            main_frame,
            width=300,
            placeholder_text="ejemplo@email.com"
        )
        self.email_input.pack()

        self.password_label = ctk.CTkLabel(
            main_frame,
            text="Contraseña:",
            font=("Helvetica", 14)
        )
        self.password_label.pack(pady=(20,5))
        
        self.password_input = ctk.CTkEntry(
            main_frame,
            width=300,
            show="•",
            placeholder_text="Ingrese su contraseña"
        )
        self.password_input.pack()

        # Botones
        button_frame = ctk.CTkFrame(main_frame)
        button_frame.pack(pady=30)
        
        self.login_button = ctk.CTkButton(
            button_frame,
            text="Iniciar Sesión",
            command=self.handle_login,
            width=140,
            height=40,
            font=("Helvetica", 14)
        )
        self.login_button.pack(side="left", padx=10)
        
        self.signup_button = ctk.CTkButton(
            button_frame,
            text="Registrarse",
            command=self.handle_signup,
            width=140,
            height=40,
            font=("Helvetica", 14),
            fg_color="gray"
        )
        self.signup_button.pack(side="left", padx=10)

        # Centrar la ventana
        self.center_window()
        
        # Hacer la ventana modal
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Iniciar loop
        self.mainloop()

    def center_window(self):
        """Centra la ventana en la pantalla"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def handle_login(self):
        """Maneja el inicio de sesión"""
        try:
            response = login(
                self.email_input.get(),
                self.password_input.get()
            )
            if response.user:
                self.result = True
                self.destroy()
            else:
                self.mostrar_error(
                    "Error",
                    "Email o contraseña incorrectos"
                )
        except Exception as e:
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
        dialog = ctk.CTkInputDialog(
            text=mensaje,
            title=titulo
        )
        dialog.get_input()

    def mostrar_info(self, titulo: str, mensaje: str):
        """Muestra un diálogo informativo"""
        dialog = ctk.CTkInputDialog(
            text=mensaje,
            title=titulo
        )
        dialog.get_input()

    def on_closing(self):
        """Maneja el cierre de la ventana"""
        self.result = False
        self.destroy() 