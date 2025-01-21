'''Calendar Widget/App'''

#Modulos
import flet
from flet import *
import calendar
import datetime

#Constants
CELL_SIZE = (28, 28)
CELL_BG_COLOR = "white10"
TODAY_BG_COLOR = "teal600"

class SetCalendar(UserControl):
    def __init__(self, start_year=datetime.date.today().year):
        self.current_year = start_year #Año actual

        self.m1 = datetime.date.today().month #Mes actual
        self.m2 = self.m1 + 1 #Segundo mes

        self.click_count: list = []
        self.log_press_count: list = []

        self.current_color = "blue" #Resaltador

        self.selected_date = any #El dato seleccionado del calendario

        self.calendar_grid = Column(
            wrap=True,
            alignment=MainAxisAlignment.CENTER,
            horizontal_alignment=CrossAxisAlignment.CENTER,
        )
        super().__init__()

    def create_month_calendar(self, year):
        self.current_year = year #Año actual
        self.calendar_grid.controls: list = [] #Limpiar el grid

        for month in range(self.m1, self.m2):
            month_label = Text(
                f"{calendar.month_name[month]} {self.current_year}",
                size=14,
                weight="bold",
            )

            month_matrix = calendar.monthcalendar(self.current_year, month)
            month_grid = Column(alignment=MainAxisAlignment.CENTER)
            month_grid.controls.append(
                Row(
                    alignment=MainAxisAlignment.START,
                    controls=[month_label]
                )
            )

            weekday_labels = [
                Container(
                    width=28,
                    height=28,
                    alignment=alignment.center,
                    content=Text(
                        weekday,
                        size=12,
                        color="white54",
                    )
                )
                for weekday in ["Lun", "Mar", "Mie", "Jue", "Vie", "Sab", "Dom"]
            ]

            weekday_row = Row(controls=weekday_labels)
            month_grid.controls.append(weekday_row)

            for week in month_matrix:
                week_container = Row()
                for day in week:
                    if day ==0: #Si el dia esta vacio
                        day_container = Container(
                            width=28,
                            height=28,
                        )
                    else:
                        day_container = Container(
                            width=28,
                            height=28,
                            border=border.all(0.5, "white54"),
                            alignment=alignment.center,
                        )
                    day_lablel = Text(str(day), size=12)

                    if day == 0:
                        day_lablel = None
                    if (
                        day ==datetime.date.today().day
                        and month ==datetime.date.today().month
                        and self.current_year == datetime.date.today().year
                    ):
                        day_container.bgcolor = "teal700"
                    day_container.content = day_lablel
                    week_container.controls.append(day_container)
                month_grid.controls.append(week_container)

        self.calendar_grid.controls.append(month_grid)

        return self.calendar_grid

    def build(self):
        return self.create_month_calendar(self.current_year)

#Main
def main(page: Page):
    page.horizontal_alignment='center'
    page.vertical_alignment='center'
    page.padding=80

    #Instancias
    cal = SetCalendar()


    #Main UI
    page.add(cal)
    page.update()


if __name__ == '__main__':
    flet.app(target=main)