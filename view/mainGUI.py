import customtkinter as ctk
from PIL import Image
import tkcalendar as Calendar

app = ctk.CTk()
app.geometry("1366x768")
ctk.set_appearance_mode("dark")
app.title("KariAriel")
app.iconbitmap("assets/icono.ico")
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#!!Configuraciones
app.grid_columnconfigure(0, weight=0) #Sidebar
app.grid_columnconfigure(1, weight=1) #Contenedor principal
app.grid_rowconfigure(0, weight=1)

tabview = ctk.CTkTabview(app)

#tabview.add("Inicio")
tabview.add("Turnos")
tabview.add("Clientes")
tabview.add("Presupuesto")

#Sidebar
#sidebar = ctk.CTkFrame(app, fg_color="transparent")
#sidebar.grid(row=0, column=0, sticky="ns")
#sidebar.grid_propagate(True) #Desactiva el ajuste automático de tamaño

#Frame para mostrar turnos
turnos_frame = ctk.CTkScrollableFrame(tabview.tab("Turnos"), fg_color="transparent")


#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#!!Funciones
def animar_texto(texto, label, i=0):
    if i <= len(texto):
        label.configure(text=texto[:i])
        label.after(5, animar_texto, texto, label, i+1)

def obtener_fecha_seleccionada(event=None):
    fecha_seleccionada = calendario.selection_get()
    nuevo_texto = f"Los turnos del día {fecha_seleccionada} son:"
    animar_texto(nuevo_texto, label_turnos)

def ocultar_inicio():
    logo_inicio_label.pack_forget()  # Oculta el logo al cambiar de pestaña
    boton_entrar.pack_forget()  # Oculta el botón de entrar al cambiar de pestaña
    tabview.pack(fill="both", expand=True, padx=20, pady=10)

def on_tab_click(event):
    if tabview.tab("Inicio") == event.widget:
        logo_inicio_label.pack(pady=20, padx=20, anchor="center")
    else:
        ocultar_inicio(event)

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#!!Botones
# Botón de entrar
boton_entrar = ctk.CTkButton(app, text="Entrar", command=ocultar_inicio)

#Calendario
calendario = Calendar.Calendar(tabview.tab("Turnos"), selectmode='day', date_pattern='yyyy-mm-dd', showweeknumbers=False, firstweekday='sunday', 
    locale='es_ES', showothermonthdays=False,
    background="#252525", disabledbackground="#252525", bordercolor="#252525",
    headersbackground="#252525",   # Fondo de encabezados (días de la semana)
    normalbackground="#252525",    # Fondo de días normales
    foreground="#ffffff",          # Color de texto (números)
    normalforeground="#cfcfd4",    # Color de días normales
    headersforeground="#ffffff",   # Texto en encabezados (días de la semana)
    weekendbackground="#252525",   # Fondo de fines de semana
    weekendforeground="#ffffff",   # Texto de fines de semana (puede ser dorado claro)
    selectbackground="#003e6f",    # Fondo del día seleccionado (azul más fuerte)
    #selectforeground="#ffffff",    # Texto del día seleccionado
    othermonthbackground="#252525", # Fondo para días de otros meses
    othermonthforeground="#6c6c80", # Texto para días de otros meses
    )

fecha_seleccionada = calendario.get_date() 

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#!!Eventos
calendario.bind("<<CalendarSelected>>", obtener_fecha_seleccionada) #Evento para obtener la fecha seleccionada

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#!!Posicionamiento
logo_inicio = ctk.CTkImage(Image.open("assets/icono.png"), size=(300, 300))
logo_inicio_label = ctk.CTkLabel(app, text="Bienvenido/a a\n KariAriel", image=logo_inicio, fg_color="transparent", font=("Bahnschrift", 40), compound="top")
logo_inicio_label.pack(pady=20, padx=20, anchor="center")
boton_entrar.pack(pady=20)

label_turnos = ctk.CTkLabel(tabview.tab("Turnos"), text=(f"Turnos del día {fecha_seleccionada}"), font=("Bahnschrift", 40))
label_turnos.pack(pady=1)

label_clientes = ctk.CTkLabel(tabview.tab("Clientes"), text="Lista de clientes", font=("Bahnschrift", 40))
label_clientes.pack(pady=10)

label_presupuesto = ctk.CTkLabel(tabview.tab("Presupuesto"), text=f"Presupuesto del día {fecha_seleccionada}", font=("Bahnschrift", 40))
label_presupuesto.pack(pady=10)

calendario.pack(pady=1, padx=20, expand=True)

turnos_frame.pack(fill="both", expand=True, padx=20, pady=10) #Frame para mostrar turnos
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
app.mainloop()