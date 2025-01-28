import flet as ft
from flet import *
from datetime import datetime, time
from models.turno import Turno
from services.turno_service import TurnoService

class ModificarTurno(UserControl):
    def __init__(self, parent, turno_service: TurnoService):
        super().__init__()
        self.parent = parent
        self.turno_service = turno_service
        self.page = None
        self.turno_actual = None
        
        # Horarios disponibles (de 8:00 a 20:00, cada 15 minutos)
        self.horas = [f"{h:02d}" for h in range(8, 21)]
        self.minutos = ["00", "15", "30", "45"]
        
        # Lista de servicios disponibles
        self.servicios_disponibles = [
            "Pin de carga",
            "Modulo",
            "Vidrio",
            "Revision",
            "Mojado",
            "Otros"
        ]

    def set_page(self, page):
        """Establece la referencia a la página de Flet"""
        self.page = page

    def editar_turno(self, turno: Turno):
        if not self.page:
            self.page = self.parent.page
            
        self.turno_actual = turno
        
        # Convertir string de servicios a lista
        servicios_actuales = turno.tipo_de_reparacion.split(", ") if turno.tipo_de_reparacion else []
        
        # Crear checkboxes para cada servicio
        self.checkboxes_servicios = [
            Checkbox(
                label=servicio,
                value=servicio in servicios_actuales,
                fill_color=colors.BLUE
            ) for servicio in self.servicios_disponibles
        ]
        
        # Crear dropdowns para hora y minutos
        hora_actual = turno.fecha_hora.hour
        minuto_actual = turno.fecha_hora.minute
        
        self.hora_dropdown = Dropdown(
            label="Hora",
            width=120,
            height=50,
            value=f"{hora_actual:02d}",
            options=[dropdown.Option(hora) for hora in self.horas],
            on_change=self.validar_hora
        )
        
        self.minuto_dropdown = Dropdown(
            label="Minutos",
            width=120,
            height=50,
            value=f"{minuto_actual:02d}",
            options=[dropdown.Option(minuto) for minuto in self.minutos],
            on_change=self.validar_hora
        )
        
        # Mensaje de error para la hora
        self.mensaje_error_hora = Text(
            color=colors.ERROR,
            size=14,
            visible=False
        )
        
        dialog = AlertDialog(
            title=Text("Modificar Turno"),
            content=Container(
                width=400,
                padding=padding.all(20),
                content=Column(
                    spacing=20,
                    controls=[
                        TextField(
                            label="Nombre",
                            value=turno.nombre,
                            width=300,
                            height=50,
                            text_size=16
                        ),
                        Container(
                            content=Column(
                                spacing=10,
                                controls=[
                                    Text(
                                        "Servicios",
                                        size=16,
                                        weight=FontWeight.BOLD
                                    ),
                                    Column(controls=self.checkboxes_servicios)
                                ]
                            )
                        ),
                        Container(
                            content=Column(
                                spacing=5,
                                controls=[
                                    Text(
                                        "Horario",
                                        size=16,
                                        weight=FontWeight.BOLD
                                    ),
                                    Row(
                                        spacing=10,
                                        alignment=MainAxisAlignment.CENTER,
                                        controls=[
                                            self.hora_dropdown,
                                            Text(":", size=20),
                                            self.minuto_dropdown,
                                        ]
                                    ),
                                    self.mensaje_error_hora
                                ]
                            )
                        ),
                        Checkbox(
                            label="Telefono reparado",
                            value=turno.confirmado,
                            on_change=lambda e: setattr(self.turno_actual, 'confirmado', e.control.value)
                        ),
                    ]
                )
            ),
            actions=[
                TextButton(
                    text="Cancelar",
                    style=ButtonStyle(color=colors.BLUE_GREY),
                    on_click=self.cerrar_dialogo
                ),
                TextButton(
                    text="Guardar",
                    style=ButtonStyle(color=colors.BLUE),
                    on_click=self.guardar_modificacion
                )
            ],
            actions_alignment=MainAxisAlignment.END
        )
        
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def validar_hora(self, e):
        """Valida que la hora seleccionada sea válida"""
        if self.hora_dropdown.value and self.minuto_dropdown.value:
            hora = int(self.hora_dropdown.value)
            minuto = int(self.minuto_dropdown.value)
            
            if hora < 8 or (hora == 20 and minuto > 0) or hora > 20:
                self.mensaje_error_hora.value = "El horario de atención es de 8:00 a 20:00"
                self.mensaje_error_hora.visible = True
            else:
                self.mensaje_error_hora.visible = False
                
        self.page.update()

    def confirmar_turno(self, turno: Turno):
        try:
            turno.confirmado = "true"
            self.turno_service.modificar_turno(turno)
            if hasattr(self.parent, 'cargar_turnos'):
                self.parent.cargar_turnos()
            return True
        except Exception as ex:
            print(f"Error al confirmar turno: {str(ex)}")
            return False

    def cerrar_dialogo(self, e):
        self.page.dialog.open = False
        self.page.update()

    def guardar_modificacion(self, e):
        try:
            # Obtener los valores actualizados de los campos
            controles = self.page.dialog.content.content.controls
            nombre = controles[0].value
            
            # Obtener servicios seleccionados
            servicios_seleccionados = [
                checkbox.label
                for checkbox in self.checkboxes_servicios
                if checkbox.value
            ]
            
            if not servicios_seleccionados:
                self.mostrar_mensaje(
                    "Error",
                    "Debe seleccionar al menos un servicio",
                    es_error=True
                )
                return False
            
            # Validar hora
            if not self.hora_dropdown.value or not self.minuto_dropdown.value:
                self.mostrar_mensaje(
                    "Error",
                    "Por favor, seleccione una hora válida",
                    es_error=True
                )
                return False

            # Crear objeto time con la hora seleccionada
            hora_seleccionada = time(
                hour=int(self.hora_dropdown.value),
                minute=int(self.minuto_dropdown.value)
            )

            # Actualizar el turno
            self.turno_actual.nombre = nombre
            self.turno_actual.tipo_de_reparacion = ", ".join(servicios_seleccionados)
            self.turno_actual.fecha_hora = datetime.combine(
                self.turno_actual.fecha_hora.date(),
                hora_seleccionada
            )

            # Guardar en la base de datos
            self.turno_service.modificar_turno(self.turno_actual)
            
            self.cerrar_dialogo(e)
            self.mostrar_mensaje(
                "Éxito",
                "Turno modificado correctamente"
            )
            
            if hasattr(self.parent, 'cargar_turnos'):
                self.parent.cargar_turnos()
            return True
        except Exception as ex:
            print(f"Error al modificar turno: {str(ex)}")
            self.mostrar_mensaje(
                "Error",
                f"No se pudo modificar el turno: {str(ex)}",
                es_error=True
            )
            return False

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