# view/frames/clientes_frame.py
import customtkinter as ctk
from config.db_queries import obtener_todos_los_clientes, buscar_clientes_por_dni
from model.Clientes import Cliente
import threading
import time

class TarjetaCliente(ctk.CTkFrame):
    def __init__(self, parent, cliente_data):
        super().__init__(parent, fg_color="transparent")
        
        # Crear cliente desde datos
        cliente = Cliente.from_dict(cliente_data)
        
        # Frame principal de la tarjeta
        self.tarjeta = ctk.CTkFrame(self, corner_radius=10, fg_color=("gray90", "gray20"))
        self.tarjeta.pack(fill="x", padx=10, pady=5)
        
        # Contenido de la tarjeta
        contenido_frame = ctk.CTkFrame(self.tarjeta, fg_color="transparent")
        contenido_frame.pack(fill="x", padx=15, pady=15)
        
        # Nombre del cliente
        nombre_label = ctk.CTkLabel(
            contenido_frame, 
            text=cliente.nombre_apellido,
            font=("Bahnschrift", 18, "bold"),
            text_color=("black", "white")
        )
        nombre_label.pack(anchor="w", pady=(0, 5))
        
        # DNI
        dni_label = ctk.CTkLabel(
            contenido_frame,
            text=f"DNI: {str(cliente.dni)}",  # Convertir a string solo para display
            font=("Bahnschrift", 14),
            text_color=("gray50", "gray70")
        )
        dni_label.pack(anchor="w", pady=(0, 3))
        
        # Teléfono (si existe)
        if cliente.telefono:
            telefono_label = ctk.CTkLabel(
                contenido_frame,
                text=f"Telefono: {cliente.telefono}",
                font=("Bahnschrift", 14),
                text_color=("gray50", "gray70")
            )
            telefono_label.pack(anchor="w", pady=(0, 3))
        
        # Email (si existe)
        if cliente.email:
            email_label = ctk.CTkLabel(
                contenido_frame,
                text=f"Email: {cliente.email}",
                font=("Bahnschrift", 14),
                text_color=("gray50", "gray70")
            )
            email_label.pack(anchor="w", pady=(0, 3))
        
        # Dirección (si existe)
        if cliente.direccion:
            direccion_label = ctk.CTkLabel(
                contenido_frame,
                text=f"Dirección: {cliente.direccion}",
                font=("Bahnschrift", 14),
                text_color=("gray50", "gray70")
            )
            direccion_label.pack(anchor="w")

class ClientesFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Variables para el debounce del buscador
        self.search_timer = None
        self.search_delay = 0.5  # 500ms de delay
        
        # Frame principal
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        titulo = ctk.CTkLabel(
            self.main_frame, 
            text="Lista de Clientes", 
            font=("Bahnschrift", 40, "bold")
        )
        titulo.pack(pady=(0, 20))
        
        # Frame para el buscador
        self.buscador_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.buscador_frame.pack(fill="x", pady=(0, 20))
        
        # Label del buscador
        buscador_label = ctk.CTkLabel(
            self.buscador_frame,
            text="Buscar por DNI:",
            font=("Bahnschrift", 16, "bold")
        )
        buscador_label.pack(anchor="w", pady=(0, 5))
        
        # Campo de búsqueda
        self.search_entry = ctk.CTkEntry(
            self.buscador_frame,
            placeholder_text="Ingresa el DNI del cliente...",
            font=("Bahnschrift", 14),
            height=40
        )
        self.search_entry.pack(fill="x", pady=(0, 10))
        
        # Vincular el evento de escritura
        self.search_entry.bind('<KeyRelease>', self.on_search_change)
        
        # Label para mostrar el estado de búsqueda
        self.status_label = ctk.CTkLabel(
            self.buscador_frame,
            text="",
            font=("Bahnschrift", 12),
            text_color=("gray50", "gray70")
        )
        self.status_label.pack(anchor="w")
        
        # Frame para el scroll
        self.scroll_frame = ctk.CTkScrollableFrame(
            self.main_frame,
            fg_color="transparent",
            width=800,
            height=500
        )
        self.scroll_frame.pack(fill="both", expand=True)
        
        # Cargar clientes iniciales
        self.cargar_clientes()
    
    def on_search_change(self, event):
        """Se ejecuta cada vez que cambia el texto de búsqueda"""
        # Cancelar búsqueda anterior si existe
        if self.search_timer:
            self.search_timer.cancel()
        
        search_term = self.search_entry.get().strip()
        
        if len(search_term) < 1:
            # Si el campo está vacío, mostrar todos los clientes
            self.cargar_clientes()
            self.status_label.configure(text="")
            return
        
        # Intentar convertir a int para búsqueda
        try:
            dni_int = int(search_term)
            # Mostrar estado de búsqueda
            self.status_label.configure(text="Buscando...")
            
            # Programar nueva búsqueda con delay
            self.search_timer = threading.Timer(self.search_delay, 
                                              lambda: self.perform_search(dni_int))
            self.search_timer.start()
        except ValueError:
            # Si no es un número válido, mostrar error
            self.status_label.configure(text="Por favor ingresa solo números para el DNI")
            self.clear_results()
    
    def perform_search(self, search_term: int):
        """Ejecuta la búsqueda de clientes por DNI"""
        try:
            # Búsqueda directa por DNI como int
            clientes_data = buscar_clientes_por_dni(search_term)
            
            # Actualizar UI en el hilo principal
            self.after(0, lambda: self.display_search_results(clientes_data, str(search_term)))
            
        except Exception as e:
            self.after(0, lambda: self.show_search_error(str(e)))
    
    def display_search_results(self, clientes_data, search_term: str):
        """Muestra los resultados de búsqueda"""
        # Limpiar contenido anterior
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        
        if not clientes_data:
            self.status_label.configure(text=f"No se encontraron clientes con DNI '{search_term}'")
            self.mostrar_mensaje_vacio()
            return
        
        self.status_label.configure(text=f"Se encontraron {len(clientes_data)} cliente(s) con DNI '{search_term}'")
        
        # Crear tarjetas para cada cliente encontrado
        for cliente_data in clientes_data:
            tarjeta = TarjetaCliente(self.scroll_frame, cliente_data)
            tarjeta.pack(fill="x", pady=5)
    
    def show_search_error(self, error_msg: str):
        """Muestra un error en la búsqueda"""
        self.status_label.configure(text=f"Error en la búsqueda: {error_msg}")
        self.clear_results()
    
    def clear_results(self):
        """Limpia los resultados mostrados"""
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
    
    def cargar_clientes(self):
        """Carga los clientes desde la base de datos"""
        def cargar_en_hilo():
            try:
                # Obtener clientes de la base de datos
                clientes_data = obtener_todos_los_clientes()
                
                if clientes_data:
                    # Limpiar contenido anterior
                    for widget in self.scroll_frame.winfo_children():
                        widget.destroy()
                    
                    # Crear tarjetas para cada cliente
                    for cliente_data in clientes_data:
                        tarjeta = TarjetaCliente(self.scroll_frame, cliente_data)
                        tarjeta.pack(fill="x", pady=5)
                    
                    # Mostrar mensaje si no hay clientes
                    if not clientes_data:
                        self.mostrar_mensaje_vacio()
                else:
                    self.mostrar_mensaje_vacio()
                    
            except Exception as e:
                print(f"Error cargando clientes: {e}")
                self.mostrar_mensaje_error()
        
        # Ejecutar en hilo separado para no bloquear la UI
        threading.Thread(target=cargar_en_hilo, daemon=True).start()
    
    def mostrar_mensaje_vacio(self):
        """Muestra mensaje cuando no hay clientes"""
        mensaje = ctk.CTkLabel(
            self.scroll_frame,
            text="No hay clientes registrados",
            font=("Bahnschrift", 18),
            text_color=("gray50", "gray70")
        )
        mensaje.pack(pady=50)
    
    def mostrar_mensaje_error(self):
        """Muestra mensaje de error"""
        mensaje = ctk.CTkLabel(
            self.scroll_frame,
            text="Error al cargar los clientes",
            font=("Bahnschrift", 18),
            text_color=("red", "orange")
        )
        mensaje.pack(pady=50)
