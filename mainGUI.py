import customtkinter as ctk
from view.frames.home_frame import HomeFrame
from view.frames.turnos_frame import TurnosFrame
from view.frames.clientes_frame import ClientesFrame
from view.frames.presupuesto_frame import PresupuestoFrame
from view.components.sidebar import Sidebar
import util.util_ventana as util_ventana
import util.util_imagenes as util_imagenes

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#!!Funciones
def mostrar_home():
    ocultar_todos_los_frames()
    home_frame.pack(expand=True, fill="both")

def mostrar_turnos():
    ocultar_todos_los_frames()
    turnos_frame = TurnosFrame(contenedor)
    turnos_frame.pack(expand=True, fill="both")

def mostrar_clientes():
    ocultar_todos_los_frames()
    clientes_frame = ClientesFrame(contenedor)
    clientes_frame.pack(expand=True, fill="both")

def mostrar_presupuesto():
    ocultar_todos_los_frames()
    presupuesto_frame = PresupuestoFrame(contenedor)
    presupuesto_frame.pack(expand=True, fill="both")

def ocultar_todos_los_frames():
    for widget in contenedor.winfo_children():
        widget.grid_forget()
        widget.pack_forget()

def animar_texto(texto, label, i=0):
    if i <= len(texto):
        label.configure(text=texto[:i])
        label.after(5, animar_texto, texto, label, i+1)
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#!!Configuraciones de la ventana
app = ctk.CTk()
w, h = 1366, 768
util_ventana.centrar_ventana(app, w, h) #Centrar ventana
ctk.set_appearance_mode("dark")
app.title("KariAriel")
app.iconbitmap("assets/icono.ico")

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#!!Configuraciones
app.grid_columnconfigure(0, weight=0) #Sidebar
app.grid_columnconfigure(1, weight=1) #Contenedor principal
app.grid_rowconfigure(0, weight=1)

#Sidebar
sidebar = Sidebar(
    master=app,
    callback_dict={
        "inicio": mostrar_home,
        "turnos": mostrar_turnos,
        "clientes": mostrar_clientes,
        "presupuesto": mostrar_presupuesto
    }
)
sidebar.grid(row=0, column=0, sticky="ns")
sidebar.grid_propagate(True)

#Contenedor principal
contenedor = ctk.CTkFrame(app, fg_color="transparent")
contenedor.grid(row=0, column=1, sticky="nsew")

# Crear el frame de inicio
home_frame = HomeFrame(contenedor, on_enter=mostrar_turnos)
home_frame.pack(expand=True, fill="both")
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
app.mainloop()