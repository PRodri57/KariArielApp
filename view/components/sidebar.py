import customtkinter as ctk
from PIL import Image
import utils.util_imagenes as util_imagenes

class Sidebar(ctk.CTkFrame):
    def __init__(self, master, callback_dict, **kwargs):
        super().__init__(master, width=60, corner_radius=0, fg_color="#1a1a1a", **kwargs)

        self.expanded = False
        self.expanded_width = 200
        self.collapsed_width = 60
        self.animation_speed = 30
        self.animation_delay = 10
        self.callback_dict = callback_dict

        self.grid_propagate(False)

        # Botón de menú (hamburguesa)
        self.menu_icon = util_imagenes.leer_imagen("assets/menu.png", (25, 25))
        self.toggle_button = ctk.CTkButton(self, image=self.menu_icon, text="", width=30, command=self.toggle_sidebar,
                                           fg_color="transparent", hover_color="#333333", compound="left",)
        self.toggle_button.grid(row=0, column=0, padx=10, pady=10, )

        # Contenedor para botones de navegación
        self.buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.buttons_frame.grid(row=1, column=0, sticky="n")

        # Diccionario de íconos y botones
        self.buttons = {
            "inicio": ("Inicio", "assets/home.png"),
            "turnos": ("Turnos", "assets/turnos.png"),
            "clientes": ("Clientes", "assets/clientes.png"),
            "presupuesto": ("Presupuesto", "assets/presupuesto.png"),
        }

        self.button_widgets = {}
        for i, (key, (text, icon_path)) in enumerate(self.buttons.items()):
            icon = util_imagenes.leer_imagen(icon_path, (25, 25))
            button = ctk.CTkButton(
                self.buttons_frame,
                text=text,
                image=icon,
                anchor="w",
                height=40,
                font=("Bahnschrift", 18),
                fg_color="transparent",
                hover_color="#2a2a2a",
                text_color="#ffffff",
                corner_radius=12,
                command=callback_dict[key]
            )
            button.grid(row=i, column=0, padx=10, pady=10, sticky="ew")
            self.button_widgets[key] = button

        self.set_button_texts(visible=False)
        self.update_button_widths(self.collapsed_width)

    def toggle_sidebar(self):
        if self.expanded:
            self.collapse()
        else:
            self.expand()

    def expand(self, current_width=None):
        if current_width is None:
            current_width = self.collapsed_width
        if current_width < self.expanded_width:
            self.configure(width=current_width)
            self.update_button_widths(current_width)
            self.after(self.animation_delay, lambda: self.expand(current_width + self.animation_speed))
        else:
            self.configure(width=self.expanded_width)
            self.update_button_widths(self.expanded_width)
            self.set_button_texts(True)
            self.expanded = True

    def collapse(self, current_width=None):
        if current_width is None:
            current_width = self.expanded_width
        if current_width > self.collapsed_width:
            self.configure(width=current_width)
            self.update_button_widths(current_width)
            if current_width - self.animation_speed <= self.collapsed_width:
                self.set_button_texts(False)
            self.after(self.animation_delay, lambda: self.collapse(current_width - self.animation_speed))
        else:
            self.configure(width=self.collapsed_width)
            self.update_button_widths(self.collapsed_width)
            self.expanded = False

    def set_button_texts(self, visible):
        for key, button in self.button_widgets.items():
            button.configure(text=self.buttons[key][0] if visible else "")

    def update_button_widths(self, width):
        for button in self.button_widgets.values():
            button.configure(width=width)
