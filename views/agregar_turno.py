import flet as ft
from flet import *
from datetime import datetime, time
from models.turno import Turno
from services.turno_service import TurnoService

class AgregarTurno(UserControl):
    def __init__(self, parent, turno_service: TurnoService):
        super().__init__()
        self.parent = parent
        self.turno_service = turno_service
        self.page = None
        self.fecha_seleccionada = None
        
        # Horarios disponibles (de 8:00 a 20:00, cada 15 minutos)
        self.horas = [f"{h:02d}" for h in range(8, 21)]
        self.minutos = ["00", "15", "30", "45"]
        self.hora_seleccionada = None
        self.minuto_seleccionado = None

    def set_page(self, page):
        """Establece la referencia a la página de Flet"""
        self.page = page

    def mostrar_dialogo_nuevo_turno(self, fecha_seleccionada):
        if not self.page:
            self.page = self.parent.page
            
        self.fecha_seleccionada = fecha_seleccionada
        
        # Crear referencias para acceder a los valores después
        self.nombre_input = TextField(
            label="Nombre",
            width=300,
            height=50,
            text_size=16,
            border_color=colors.BLUE_GREY_400
        )
        
        self.servicio_dropdown = Dropdown(
            label="Tipo de servicio",
            width=300,
            height=50,
            text_size=16,
            options=[
                dropdown.Option("Pin de carga"),
                dropdown.Option("Modulo"),
                dropdown.Option("Vidrio"),
                dropdown.Option("Revision"),
                dropdown.Option("Mojado"),
                dropdown.Option("Otros")
            ],
            border_color=colors.BLUE_GREY_400
        )
        
        # Crear selectores de hora y minutos
        self.hora_dropdown = Dropdown(
            label="Hora",
            width=120,
            height=50,
            text_size=16,
            options=[dropdown.Option(hora) for hora in self.horas],
            on_change=self.validar_hora,
            border_color=colors.BLUE_GREY_400
        )
        
        self.minuto_dropdown = Dropdown(
            label="Minutos",
            width=120,
            height=50,
            text_size=16,
            options=[dropdown.Option(minuto) for minuto in self.minutos],
            on_change=self.validar_hora,
            border_color=colors.BLUE_GREY_400
        )
        
        # Contenedor para mensaje de error de hora
        self.mensaje_error_hora = Text(
            color=colors.ERROR,
            size=14,
            visible=False
        )
            
        dialog = AlertDialog(
            title=Text(
                "Nuevo Turno",
                size=24,
                weight=FontWeight.BOLD,
                color=colors.BLUE_GREY
            ),
            content=Container(
                width=400,
                padding=padding.all(20),
                content=Column(
                    spacing=20,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    controls=[
                        self.nombre_input,
                        self.servicio_dropdown,
                        Container(
                            content=Column(
                                spacing=5,
                                controls=[
                                    Text(
                                        "Horario",
                                        size=16,
                                        color=colors.BLUE_GREY
                                    ),
                                    Row(
                                        spacing=10,
                                        alignment=MainAxisAlignment.CENTER,
                                        controls=[
                                            self.hora_dropdown,
                                            Text(":", size=20),
                                            self.minuto_dropdown,
                                        ]
                                    )
                                ]
                            )
                        ),
                        self.mensaje_error_hora
                    ]
                )
            ),
            actions=[
                TextButton(
                    text="Cancelar",
                    style=ButtonStyle(
                        color=colors.BLUE_GREY,
                        padding=padding.all(20)
                    ),
                    on_click=self.cerrar_dialogo
                ),
                TextButton(
                    text="Guardar",
                    style=ButtonStyle(
                        color=colors.BLUE,
                        padding=padding.all(20)
                    ),
                    on_click=self.guardar_turno
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
            
            # Validar horario de atención (8:00 a 20:00)
            if hora < 8 or (hora == 20 and minuto > 0) or hora > 20:
                self.mensaje_error_hora.value = "El horario de atención es de 8:00 a 20:00"
                self.mensaje_error_hora.visible = True
            else:
                self.mensaje_error_hora.visible = False
                self.hora_seleccionada = hora
                self.minuto_seleccionado = minuto
                
        self.page.update()

    def cerrar_dialogo(self, e):
        self.page.dialog.open = False
        self.page.update()

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

    def guardar_turno(self, e):
        try:
            # Validar campos
            nombre = self.nombre_input.value
            tipo_de_reparacion = self.servicio_dropdown.value
            
            if not nombre or not tipo_de_reparacion:
                self.mostrar_mensaje(
                    "Error",
                    "Por favor, complete todos los campos",
                    es_error=True
                )
                return
                
            if not self.hora_dropdown.value or not self.minuto_dropdown.value:
                self.mostrar_mensaje(
                    "Error",
                    "Por favor, seleccione una hora válida",
                    es_error=True
                )
                return

            # Crear objeto time con la hora seleccionada
            hora_seleccionada = time(
                hour=int(self.hora_dropdown.value),
                minute=int(self.minuto_dropdown.value)
            )

            # Crear objeto datetime combinando fecha y hora
            fecha_hora = datetime.combine(
                self.fecha_seleccionada,
                hora_seleccionada
            )

            # Crear nuevo turno
            nuevo_turno = Turno(
                nombre=nombre,
                tipo_de_reparacion=tipo_de_reparacion,
                fecha_hora=fecha_hora,
                confirmado="false"
            )

            # Imprimir para debugging
            print(f"Guardando turno: {nuevo_turno.__dict__}")

            # Guardar en la base de datos
            self.turno_service.agregar_turno(nuevo_turno)
            
            # Cerrar diálogo y mostrar mensaje de éxito
            self.cerrar_dialogo(e)
            self.mostrar_mensaje(
                "Éxito",
                "Turno agregado correctamente"
            )
            
            # Actualizar la lista de turnos
            if hasattr(self.parent, 'cargar_turnos'):
                self.parent.cargar_turnos()
                
            return True

        except Exception as ex:
            print(f"Error al guardar turno: {str(ex)}")
            self.mostrar_mensaje(
                "Error",
                f"No se pudo guardar el turno: {str(ex)}",
                es_error=True
            )
            return False