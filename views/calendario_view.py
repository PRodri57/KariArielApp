import flet as ft
from flet import *
import calendar
import datetime
from typing import Dict, List, Optional
from models.turno import Turno
from services.turno_service import TurnoService
from views.agregar_turno import AgregarTurno
from views.eliminar_turno import EliminarTurno
from views.modificar_turno import ModificarTurno

class CalendarioView(UserControl):
    # Mapeo de colores para tipos de servicio - constante de clase
    COLORES_SERVICIO = {
        "Pin de carga": colors.PURPLE_200,
        "Modulo": colors.RED_200,
        "Vidrio": colors.BLUE_200,
        "Revision": colors.GREEN_200,
        "Mojado": colors.ORANGE_200,
        "Otros": colors.GREY_200,
    }
    
    # Días de la semana - constante de clase
    DIAS_SEMANA = ["Dom", "Lun", "Mar", "Mie", "Jue", "Vie", "Sab"]

    def __init__(self, turno_service: TurnoService):
        super().__init__()
        self.turno_service = turno_service
        self.today = datetime.date.today()
        self.current_year = self.today.year
        self.current_month = self.today.month
        self.selected_date = self.today
        self.selected_container = None
        self.page = None
        self.turnos_list = None
        
        # Inicializar primer día de la semana
        calendar.setfirstweekday(calendar.SUNDAY)

        # Inicializar manejadores de turnos
        self._init_handlers()

    def _init_handlers(self):
        """Inicializa los manejadores de turnos"""
        self.agregar_turno = AgregarTurno(self, self.turno_service)
        self.eliminar_turno = EliminarTurno(self, self.turno_service)
        self.modificar_turno = ModificarTurno(self, self.turno_service)

    def build(self):
        """Construye la interfaz de usuario - método requerido por UserControl"""
        # Crear la lista de turnos
        self.turnos_list = ListView(
            expand=True,
            spacing=10,
            padding=20,
            height=600,
        )
        
        # Crear el calendario
        calendar_view = self._create_calendar()
        
        # Crear el contenedor principal
        return Row(
            controls=[
                # Panel izquierdo (Calendario)
                Container(
                    width=400,
                    padding=20,
                    content=Column(
                        controls=[
                            calendar_view,
                            self._create_new_appointment_button()
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

    def _create_new_appointment_button(self):
        """Crea el botón para agregar un nuevo turno"""
        return ElevatedButton(
            text="Nuevo Turno",
            on_click=self.mostrar_dialogo_nuevo_turno,
            style=ButtonStyle(
                color={
                    MaterialState.DEFAULT: colors.WHITE,
                },
                bgcolor={
                    MaterialState.DEFAULT: colors.TEAL_700,
                }
            )
        )

    def run(self):
        """Inicia la aplicación Flet"""
        def main(page: ft.Page):
            # Configurar la página
            self._configure_page(page)
            
            # Establecer referencias a la página
            self.page = page
            self._set_page_references(page)
            
            # Agregar el contenido a la página
            page.add(self.build())
            
            # Cargar los turnos iniciales
            self.cargar_turnos()
            page.update()

            # Configurar el evento de cierre de ventana
            self._setup_window_close_event(page)

        ft.app(target=main)

    def _configure_page(self, page: ft.Page):
        """Configura los atributos de la página"""
        page.title = "Gestor de Turnos"
        page.window_width = 1200
        page.window_height = 800
        page.window_resizable = True
        page.window_maximizable = True
        page.theme_mode = ThemeMode.DARK
        page.padding = 0
        page.window_prevent_close = False

    def _set_page_references(self, page: ft.Page):
        """Establece referencias a la página en los manejadores"""
        self.agregar_turno.set_page(page)
        self.eliminar_turno.set_page(page)
        self.modificar_turno.set_page(page)

    def _setup_window_close_event(self, page: ft.Page):
        """Configura el evento de cierre de ventana"""
        def window_event(e):
            if e.data == "close":
                page.window_destroy()
        page.window_event = window_event
    
    def previous_month(self, e):
        """Navega al mes anterior"""
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self.update_calendar()

    def next_month(self, e):
        """Navega al mes siguiente"""
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        self.update_calendar()

    def update_calendar(self):
        """Actualiza la vista del calendario"""
        if not self.page:
            return
            
        calendar_view = self._create_calendar()
        self.page.controls[0].controls[0].content.controls[0] = calendar_view
        self.page.update()

    def _create_calendar(self):
        """Crea la vista del calendario"""
        calendar_grid = Column(
            wrap=True,
            alignment=MainAxisAlignment.CENTER,
            horizontal_alignment=CrossAxisAlignment.CENTER,
        )

        # Crear la navegación del mes
        month_navigation = self._create_month_navigation()

        # Crear la cuadrícula del mes
        month_grid = Column(alignment=MainAxisAlignment.CENTER)
        month_grid.controls.append(
            Row(
                alignment=MainAxisAlignment.CENTER,
                controls=[month_navigation]
            )
        )

        # Agregar los días de la semana
        month_grid.controls.append(self._create_weekday_labels())

        # Agregar los días del mes
        month_matrix = calendar.monthcalendar(self.current_year, self.current_month)
        for week in month_matrix:
            month_grid.controls.append(self._create_week_row(week))
        
        calendar_grid.controls.append(month_grid)
        return calendar_grid

    def _create_month_navigation(self):
        """Crea la navegación del mes"""
        month_label = Text(
            f"{calendar.month_name[self.current_month]} {self.current_year}",
            size=16,
            weight="bold",
        )

        return Row(
            alignment=MainAxisAlignment.CENTER,
            controls=[
                IconButton(
                    on_click=self.previous_month,
                    icon=ft.Icons.ARROW_BACK,
                ),
                month_label,
                IconButton(
                    on_click=self.next_month,
                    icon=ft.Icons.ARROW_FORWARD,
                )
            ]
        )

    def _create_weekday_labels(self):
        """Crea las etiquetas de los días de la semana"""
        return Row(
            controls=[
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
                for weekday in self.DIAS_SEMANA
            ]
        )

    def _create_week_row(self, week):
        """Crea una fila de días de la semana"""
        week_container = Row()
        for day in week:
            if day == 0:
                day_container = Container(width=40, height=40)
            else:
                day_container = self._create_day_container(day)
            week_container.controls.append(day_container)
        return week_container

    def _create_day_container(self, day):
        """Crea un contenedor para un día del mes"""
        day_container = Container(
            width=40,
            height=40,
            border=border.all(0.5, "white54"),
            alignment=alignment.center,
            on_click=lambda e, d=day: self.on_date_selected(e, d, e.control),
            animate=animation.Animation(300, "easeOut"),
            content=Text(str(day), size=14)
        )
        
        # Marcar el día actual
        if (
            day == self.today.day
            and self.current_month == self.today.month
            and self.current_year == self.today.year
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
            
        return day_container

    def on_date_selected(self, e, day, container):
        """Maneja la selección de un día en el calendario"""
        # Restaurar el color del contenedor previamente seleccionado
        if self.selected_container:
            self._restore_container_color()

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
        if self.page:
            self.page.update()
        
        # Cargar los turnos de la nueva fecha
        self.cargar_turnos()

    def _restore_container_color(self):
        """Restaura el color del contenedor previamente seleccionado"""
        # Si era el día actual, restaurar su color especial
        if (
            self.selected_date.day == self.today.day
            and self.current_month == self.today.month
            and self.current_year == self.today.year
        ):
            self.selected_container.bgcolor = "teal700"
        else:
            self.selected_container.bgcolor = None

    def cargar_turnos(self):
        """Carga los turnos para la fecha seleccionada"""
        if not self.page:
            return
            
        try:
            turnos = self.turno_service.obtener_turnos_por_fecha(self.selected_date)
            self.actualizar_lista_turnos(turnos)
        except Exception as e:
            print(f"Error al cargar turnos: {str(e)}")
            self._mostrar_error("Error al cargar turnos")

    def _mostrar_error(self, mensaje: str):
        """Muestra un mensaje de error"""
        if self.page:
            self.page.snack_bar = SnackBar(
                content=Text(mensaje),
                bgcolor=colors.RED_400
            )
            self.page.snack_bar.open = True
            self.page.update()

    def actualizar_lista_turnos(self, turnos: List[Turno]):
        """Actualiza la lista de turnos"""
        if not hasattr(self, 'turnos_list') or not self.turnos_list:
            return
            
        self.turnos_list.controls.clear()
        
        if not turnos:
            self.turnos_list.controls.append(
                Text("No hay turnos para esta fecha", italic=True, color="white54")
            )
        else:
            for turno in turnos:
                self.turnos_list.controls.append(self._crear_tarjeta_turno(turno))
        
        if self.page:
            self.page.update()

    def _crear_tarjeta_turno(self, turno: Turno) -> Card:
        """Crea una tarjeta para un turno"""
        return Card(
            content=Container(
                padding=20,
                bgcolor=self.COLORES_SERVICIO.get(turno.tipo_de_reparacion, colors.GREY_200),
                border_radius=10,
                content=Row(
                    alignment=MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        self._crear_info_turno(turno),
                        self._crear_acciones_turno(turno)
                    ]
                )
            )
        )

    def _crear_info_turno(self, turno: Turno) -> Column:
        """Crea la columna de información del turno"""
        return Column(
            spacing=5,
            controls=[
                Row(
                    alignment=MainAxisAlignment.CENTER,
                    controls=[
                        Text(
                            f"{turno.fecha_hora.strftime('%H:%M')} - {turno.nombre} \n{turno.tecnico}",
                            size=16,
                            weight=FontWeight.BOLD,
                            color=colors.BLACK
                        ),
                        IconButton(
                            icon=ft.Icons.CHECK_OUTLINED,
                            bgcolor=colors.GREEN,
                            scale=0.8,
                            visible=turno.confirmado,
                        ),
                    ]
                ),
                Text(
                    turno.tipo_de_reparacion,
                    size=14,
                    color=colors.BLACK
                ),
            ]
        )

    def _crear_acciones_turno(self, turno: Turno) -> Row:
        """Crea la fila de acciones del turno"""
        controls = [
            IconButton(
                icon=icons.EDIT,
                icon_color=colors.BLUE_GREY,
                on_click=lambda e, t=turno: self.modificar_turno_handler(t)
            ),
            IconButton(
                icon=icons.DELETE,
                icon_color=colors.RED,
                on_click=lambda e, t=turno: self.eliminar_turno_handler(t)
            )
        ]
        
        # Agregar botón de confirmar solo si no está confirmado
        if turno.confirmado != "true":
            controls.append(
                IconButton(
                    icon=icons.CHECK_CIRCLE,
                    icon_color=colors.GREEN,
                    on_click=lambda e, t=turno: self.confirmar_turno_handler(t)
                )
            )
            
        return Row(controls=controls)

    def mostrar_dialogo_nuevo_turno(self, e):
        """Muestra el diálogo para agregar un nuevo turno"""
        if self.agregar_turno.mostrar_dialogo_nuevo_turno(self.selected_date):
            self.cargar_turnos()

    def modificar_turno_handler(self, turno: Turno):
        """Maneja la edición de un turno"""
        if self.modificar_turno.editar_turno(turno):
            self.cargar_turnos()

    def confirmar_turno_handler(self, turno: Turno):
        """Maneja la confirmación de un turno"""
        if self.modificar_turno.confirmar_turno(turno):
            self.cargar_turnos()

    def eliminar_turno_handler(self, turno: Turno):
        """Maneja la eliminación de un turno"""
        if self.eliminar_turno.eliminar_turno(turno):
            self.cargar_turnos()