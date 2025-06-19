import customtkinter as ctk
from supabase import create_client, Client
import threading
import time
from typing import List, Dict, Any

class SearchAsYouType:
    def __init__(self, supabase_url: str, supabase_key: str):
        # Configurar Supabase
        self.supabase: Client = create_client(supabase_url, supabase_key)
        
        # Variables para el debounce
        self.search_timer = None
        self.search_delay = 0.5  # 500ms de delay
        
        # Configurar la ventana principal
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.root = ctk.CTk()
        self.root.geometry("800x600")
        self.root.title("Search as You Type - Supabase")
        
        # Frame principal
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        title = ctk.CTkLabel(main_frame, text="Búsqueda en Tiempo Real", 
                           font=ctk.CTkFont(size=24, weight="bold"))
        title.pack(pady=(20, 10))
        
        # Campo de búsqueda
        self.search_entry = ctk.CTkEntry(
            main_frame, 
            placeholder_text="Escribe para buscar...",
            font=ctk.CTkFont(size=14),
            height=40
        )
        self.search_entry.pack(fill="x", padx=20, pady=10)
        
        # Vincular el evento de escritura
        self.search_entry.bind('<KeyRelease>', self.on_search_change)
        
        # Label para mostrar el estado
        self.status_label = ctk.CTkLabel(main_frame, text="")
        self.status_label.pack(pady=5)
        
        # Frame para los resultados con scrollbar
        self.results_frame = ctk.CTkScrollableFrame(main_frame, height=400)
        self.results_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
    def on_search_change(self, event):
        """Se ejecuta cada vez que cambia el texto de búsqueda"""
        # Cancelar búsqueda anterior si existe
        if self.search_timer:
            self.search_timer.cancel()
        
        search_term = self.search_entry.get().strip()
        
        if len(search_term) < 2:
            self.clear_results()
            self.status_label.configure(text="")
            return
        
        # Mostrar estado de búsqueda
        self.status_label.configure(text="Buscando...")
        
        # Programar nueva búsqueda con delay
        self.search_timer = threading.Timer(self.search_delay, 
                                          lambda: self.perform_search(search_term))
        self.search_timer.start()
    
    def perform_search(self, search_term: str):
        """Ejecuta la búsqueda en Supabase"""
        try:
            # Ejemplo de búsqueda en una tabla llamada 'products'
            # Ajusta según tu esquema de base de datos
            response = self.supabase.table('products').select('*').ilike('name', f'%{search_term}%').limit(20).execute()
            
            # Actualizar UI en el hilo principal
            self.root.after(0, lambda: self.display_results(response.data, search_term))
            
        except Exception as e:
            self.root.after(0, lambda: self.show_error(str(e)))
    
    def display_results(self, results: List[Dict[Any, Any]], search_term: str):
        """Muestra los resultados en la interfaz"""
        self.clear_results()
        
        if not results:
            self.status_label.configure(text=f"No se encontraron resultados para '{search_term}'")
            return
        
        self.status_label.configure(text=f"Se encontraron {len(results)} resultados")
        
        # Crear un widget para cada resultado
        for i, item in enumerate(results):
            result_frame = ctk.CTkFrame(self.results_frame)
            result_frame.pack(fill="x", padx=5, pady=2)
            
            # Título del resultado (ajusta según tus datos)
            title = ctk.CTkLabel(
                result_frame, 
                text=item.get('name', 'Sin título'),
                font=ctk.CTkFont(size=14, weight="bold"),
                anchor="w"
            )
            title.pack(fill="x", padx=10, pady=(10, 5))
            
            # Descripción (ajusta según tus datos)
            if 'description' in item:
                desc = ctk.CTkLabel(
                    result_frame,
                    text=item['description'][:100] + "..." if len(item.get('description', '')) > 100 else item.get('description', ''),
                    font=ctk.CTkFont(size=12),
                    anchor="w",
                    text_color="gray"
                )
                desc.pack(fill="x", padx=10, pady=(0, 10))
    
    def clear_results(self):
        """Limpia los resultados mostrados"""
        for widget in self.results_frame.winfo_children():
            widget.destroy()
    
    def show_error(self, error_msg: str):
        """Muestra un error en la interfaz"""
        self.status_label.configure(text=f"Error: {error_msg}")
        self.clear_results()
    
    def run(self):
        """Inicia la aplicación"""
        self.root.mainloop()


# Ejemplo de uso con configuración más avanzada
class AdvancedSearchAsYouType(SearchAsYouType):
    def __init__(self, supabase_url: str, supabase_key: str):
        super().__init__(supabase_url, supabase_key)
        self.search_history = []
    
    def perform_search(self, search_term: str):
        """Búsqueda avanzada con múltiples tablas y filtros"""
        try:
            # Guardar en historial
            if search_term not in self.search_history:
                self.search_history.append(search_term)
            
            # Búsqueda en múltiples campos
            response = (self.supabase
                       .table('products')
                       .select('*, categories(name)')
                       .or_(f'name.ilike.%{search_term}%,description.ilike.%{search_term}%')
                       .order('created_at', desc=True)
                       .limit(15)
                       .execute())
            
            self.root.after(0, lambda: self.display_results(response.data, search_term))
            
        except Exception as e:
            self.root.after(0, lambda: self.show_error(str(e)))


# Función principal para inicializar la aplicación
def main():
    # Configura tus credenciales de Supabase
    SUPABASE_URL = "tu_supabase_url_aqui"
    SUPABASE_KEY = "tu_supabase_anon_key_aqui"
    
    try:
        # Crear y ejecutar la aplicación
        app = SearchAsYouType(SUPABASE_URL, SUPABASE_KEY)
        app.run()
    except Exception as e:
        print(f"Error al inicializar la aplicación: {e}")


if __name__ == "__main__":
    main()


# Ejemplo adicional: Configuración de búsqueda para diferentes tipos de datos
class ConfigurableSearch:
    def __init__(self, supabase_client: Client, table_name: str, search_fields: List[str]):
        self.supabase = supabase_client
        self.table_name = table_name
        self.search_fields = search_fields
    
    def build_search_query(self, search_term: str):
        """Construye una consulta de búsqueda dinámica"""
        conditions = [f"{field}.ilike.%{search_term}%" for field in self.search_fields]
        return ".or.".join(conditions)
    
    async def search(self, search_term: str, limit: int = 20):
        """Ejecuta la búsqueda configurada"""
        query = self.build_search_query(search_term)
        response = (self.supabase
                   .table(self.table_name)
                   .select('*')
                   .or_(query)
                   .limit(limit)
                   .execute())
        return response.data
    