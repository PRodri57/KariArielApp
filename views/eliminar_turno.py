import flet as ft
from flet import *
from models.turno import Turno
from services.turno_service import TurnoService

class EliminarTurno(UserControl):
    def __init__(self, parent, turno_service: TurnoService):
        super().__init__()
        self.parent = parent
        self.turno_service = turno_service
        self.page = None

    def set_page(self, page):
        """Establece la referencia a la página de Flet"""
        self.page = page

    def mostrar_mensaje(self, titulo: str, mensaje: str, es_error: bool = False):
        """Muestra un mensaje al usuario"""
        color = colors.ERROR if es_error else colors.GREEN
        dialog = AlertDialog(
            title=Text(titulo, color=color),
            content=Text(mensaje),
            actions=[
                TextButton("Aceptar", on_click=lambda e: self.cerrar_mensaje(e))
            ]
        )
        
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def cerrar_mensaje(self, e):
        self.page.dialog.open = False
        self.page.update()

    def eliminar_turno(self, turno: Turno):
        if not self.page:
            self.page = self.parent.page
            
        dialog = AlertDialog(
            modal=True,
            title=Text("Confirmar eliminación"),
            content=Text(f"¿Está seguro que desea eliminar el turno de {turno.nombre}?"),
            actions=[
                TextButton("Cancelar", on_click=self.cerrar_dialogo),
                TextButton(
                    "Eliminar",
                    on_click=lambda e: self.confirmar_eliminacion(e, turno),
                    style=ButtonStyle(color="error")
                )
            ]
        )
        
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()
        return False  # Retornamos False para que no se actualice la lista hasta que se confirme

    def cerrar_dialogo(self, e):
        self.page.dialog.open = False
        self.page.update()

    def confirmar_eliminacion(self, e, turno: Turno):
        try:
            self.turno_service.eliminar_turno(turno.id)
            self.cerrar_dialogo(e)
            self.mostrar_mensaje(
                "Éxito",
                "Turno eliminado correctamente"
            )
            if hasattr(self.parent, 'cargar_turnos'):
                self.parent.cargar_turnos()
            return True
        except Exception as ex:
            print(f"Error al eliminar turno: {str(ex)}")
            self.mostrar_mensaje(
                "Error",
                f"No se pudo eliminar el turno: {str(ex)}",
                es_error=True
            )
            return False 