import flet as ft
from flet import *
import calendar
import datetime
from typing import Dict, List
from models.turno import Turno
from services.turno_service import TurnoService
from views.agregar_turno import AgregarTurno
from views.eliminar_turno import EliminarTurno
from views.modificar_turno import ModificarTurno

class CalendarioView:
    def __init__(self, turno_service: TurnoService):
        self.turno_service = turno_service
        self.current_year = datetime.date.today().year
        self.current_month = datetime.date.today().month
        self.selected_date = datetime.date.today()
        self.selected_container = None  # Para mantener referencia al día seleccionado
        
        # Inicializar manejadores
        self.agregar_turno = AgregarTurno(self, turno_service)
        self.eliminar_turno = EliminarTurno(self, turno_service)
        self.modificar_turno = ModificarTurno(self, turno_service)
        
        # Iniciar la aplicación Flet
        ft.app(target=self.build_flet_ui)

    def build_flet_ui(self, page: ft.Page):
        self.page = page
        page.title = "Calendario"
        page.window_width = 1200
        page.window_height = 800
        page.theme_mode = ThemeMode.DARK
        
        # Pasar la referencia de la página a los componentes
        self.agregar_turno.set_page(page)
        self.eliminar_turno.set_page(page)
        self.modificar_turno.set_page(page)
        
        # Crear la lista de turnos
        self.turnos_list = ListView(
            expand=True,
            spacing=10,
            padding=20,
        )
        
        # Crear el calendario
        calendar_view = self.create_calendar()
        
        # Crear el contenedor principal
        main_content = Row(
            controls=[
                # Panel izquierdo (Calendario)
                Container(
                    width=400,
                    padding=20,
                    content=Column(
                        controls=[
                            calendar_view,
                            ElevatedButton(
                                text="Nuevo Turno",
                                on_click=self.mostrar_dialogo_nuevo_turno,
                                style=ButtonStyle(
                                    color={
                                        MaterialState.DEFAULT: colors.WHITE,
                                    },
                                    bgcolor={
                                        MaterialState.DEFAULT: colors.TEAL_700,
                                    },
                                )
                            )
                        ]
                    )
                ),
                # Panel derecho (Lista de turnos)
                Container(
                    expand=True,
                    padding=20,
                    content=Column(
                        controls=[
                            Text("Turnos del día", size=24, weight="bold"),
                            self.turnos_list
                        ]
                    )
                )
            ]
        )
        
        # Agregar el contenido a la página
        page.add(main_content)
        
        # Cargar los turnos iniciales
        self.cargar_turnos()
        page.update()

    def create_calendar(self):
        calendar_grid = Column(
            wrap=True,
            alignment=MainAxisAlignment.CENTER,
            horizontal_alignment=CrossAxisAlignment.CENTER,
        )

        month_label = Text(
            f"{calendar.month_name[self.current_month]} {self.current_year}",
            size=16,
            weight="bold",
        )

        month_matrix = calendar.monthcalendar(self.current_year, self.current_month)
        month_grid = Column(alignment=MainAxisAlignment.CENTER)
        month_grid.controls.append(
            Row(
                alignment=MainAxisAlignment.CENTER,
                controls=[month_label]
            )
        )

        # Días de la semana
        weekday_labels = [
            Container(
                width=40,
                height=40,
                alignment=alignment.center,
                content=Text(
                    weekday,
                    size=12,
                    color="white54",
                )
            )
            for weekday in ["Lun", "Mar", "Mie", "Jue", "Vie", "Sab", "Dom"]
        ]

        month_grid.controls.append(Row(controls=weekday_labels))

        # Días del mes
        for week in month_matrix:
            week_container = Row()
            for day in week:
                if day == 0:
                    day_container = Container(width=40, height=40)
                else:
                    day_container = Container(
                        width=40,
                        height=40,
                        border=border.all(0.5, "white54"),
                        alignment=alignment.center,
                        on_click=lambda e, d=day, cont=None: self.on_date_selected(e, d, e.control),
                        animate=animation.Animation(300, "easeOut")
                    )
                    
                day_label = Text(str(day) if day != 0 else "", size=14)
                
                # Marcar el día actual
                if (
                    day == datetime.date.today().day
                    and self.current_month == datetime.date.today().month
                    and self.current_year == datetime.date.today().year
                ):
                    day_container.bgcolor = "teal700"
                
                # Marcar el día seleccionado
                if (
                    day == self.selected_date.day
                    and self.current_month == self.selected_date.month
                    and self.current_year == self.selected_date.year
                ):
                    day_container.bgcolor = "blue700"
                    self.selected_container = day_container
                
                day_container.content = day_label
                week_container.controls.append(day_container)
            
            month_grid.controls.append(week_container)
        
        calendar_grid.controls.append(month_grid)
        return calendar_grid

    def on_date_selected(self, e, day, container):
        # Restaurar el color del contenedor previamente seleccionado
        if self.selected_container:
            # Si era el día actual, restaurar su color especial
            if (
                self.selected_date.day == datetime.date.today().day
                and self.current_month == datetime.date.today().month
                and self.current_year == datetime.date.today().year
            ):
                self.selected_container.bgcolor = "teal700"
            else:
                self.selected_container.bgcolor = None

        # Actualizar la fecha seleccionada
        self.selected_date = datetime.date(
            self.current_year,
            self.current_month,
            day
        )

        # Marcar el nuevo contenedor seleccionado
        container.bgcolor = "blue700"
        self.selected_container = container
        
        # Actualizar la interfaz
        self.page.update()
        
        # Cargar los turnos de la nueva fecha
        self.cargar_turnos()

    def cargar_turnos(self):
        try:
            turnos = self.turno_service.obtener_turnos_por_fecha(self.selected_date)
            self.actualizar_lista_turnos(turnos)
        except Exception as e:
            print(f"Error al cargar turnos: {str(e)}")

    def obtener_color_servicio(self, tipo_servicio: str) -> str:
        """Retorna el color correspondiente al tipo de servicio"""
        colores = {
            "Pin de carga": colors.PURPLE_200,
            "Modulo": colors.RED_200,
            "Pantalla": colors.BLUE_200,
            "Revision": colors.GREEN_200
        }
        return colores.get(tipo_servicio, colors.GREY_200)

    def actualizar_lista_turnos(self, turnos: List[Turno]):
        if not hasattr(self, 'turnos_list'):
            return
            
        self.turnos_list.controls.clear()
        
        for turno in turnos:
            turno_card = Card(
                content=Container(
                    padding=20,
                    bgcolor=self.obtener_color_servicio(turno.tipo_de_reparacion),
                    border_radius=10,
                    content=Row(
                        alignment=MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            Column(
                                spacing=5,
                                controls=[
                                    Text(
                                        f"{turno.fecha_hora.strftime('%H:%M')} - {turno.nombre}",
                                        size=16,
                                        weight=FontWeight.BOLD
                                    ),
                                    Text(
                                        turno.tipo_de_reparacion,
                                        size=14,
                                        color=colors.GREY_800
                                    )
                                ]
                            ),
                            Row(
                                controls=[
                                    IconButton(
                                        icon=icons.EDIT,
                                        icon_color=colors.BLUE_GREY,
                                        on_click=lambda e, t=turno: self.modificar_turno.editar_turno(t)
                                    ),
                                    IconButton(
                                        icon=icons.DELETE,
                                        icon_color=colors.RED,
                                        on_click=lambda e, t=turno: self.eliminar_turno.eliminar_turno(t)
                                    ),
                                    IconButton(
                                        icon=icons.CHECK_CIRCLE,
                                        icon_color=colors.GREEN,
                                        on_click=lambda e, t=turno: self.modificar_turno.confirmar_turno(t)
                                    ) if turno.confirmado != "true" else Container()
                                ]
                            )
                        ]
                    )
                )
            )
            self.turnos_list.controls.append(turno_card)
        
        self.page.update()

    def mostrar_dialogo_nuevo_turno(self, e):
        if self.agregar_turno.mostrar_dialogo_nuevo_turno(self.selected_date):
            self.cargar_turnos()

    def editar_turno(self, turno: Turno):
        if self.modificar_turno.editar_turno(turno):
            self.cargar_turnos()

    def confirmar_turno(self, turno: Turno):
        if self.modificar_turno.confirmar_turno(turno):
            self.cargar_turnos()

    def eliminar_turno(self, turno: Turno):
        if self.eliminar_turno.eliminar_turno(turno):
            self.cargar_turnos() 