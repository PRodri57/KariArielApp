from customtkinter import *
from PIL import Image

app = CTk()
app.geometry("800x600")

set_appearance_mode("dark")

img = Image.open("assets/plus.png")

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#FUNCIONES

def click_handler():
    print(f"Boton clickeado, valor obtenido: {entry.get()}")
    #label.configure(text="Clickeado!")
    #btn.configure(text="Clickeame de nuevo")

def combobox_handler(value):
    print(f"Valor seleccionado: {value}")

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#VISUALIZACION
app.title("KariAriel")
app.iconbitmap("assets/home.ico")

#TAB
tabview = CTkTabview(master=app, corner_radius=32, fg_color="transparent", border_color="#D4C9BE", border_width=2)
tabview.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
tabview.grid_columnconfigure(0, weight=1)

tabview.add("Tab 1")
tabview.add("Tab 2")
tabview.add("Tab 3")

#FRAMES
frame = CTkFrame(app, fg_color="transparent", corner_radius=32, border_color="#D4C9BE", border_width=2)
frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
frame.grid_columnconfigure(1, weight=1)

frame2 = CTkScrollableFrame(master=tabview.tab("Tab 2"), fg_color="transparent", corner_radius=32, border_color="#D4C9BE", border_width=2, height=200, width=400)
frame2.grid(row=12, column=1, padx=20, pady=20)
frame2.place(relx=0.5, rely=0.5, anchor="center")


#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#BOTON CON IMAGEN
btn = CTkButton(master=frame, text="Clickeame", corner_radius=32, fg_color="transparent", hover_color="#98D2C0", text_color="#F1EFEC", 
                border_color="#D4C9BE", border_width=2, image=CTkImage(img), command=click_handler, font=("Helvetica", 12))
btn.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

#LABEL
label = CTkLabel(master=tabview.tab("Tab 3"), text="Algo q pinto escribir...", font=("Helvetica", 40))
label.place(relx=0.5, rely=0.15, anchor="center")

#COMBOBOX
combobox = CTkComboBox(master=tabview.tab("Tab 3"), values=["Abecedario", "Numeros", "Colores"], fg_color="black", corner_radius=32, command=combobox_handler)
combobox.set("Selecciona una opción")
combobox.place(relx=0.2, rely=0.5, anchor="center")

#CHECKBOX
checkbox = CTkCheckBox(tabview.tab("Tab 2"), text="Estado", fg_color="black", text_color="white")
checkbox.place(relx=0.5, rely=0.5, anchor="center")

#SWITCH
switch = CTkSwitch(master=tabview.tab("Tab 3"), text="Estado", fg_color="black", text_color="white", corner_radius=32)
switch.place(relx=0.8, rely=0.6, anchor="center")

#SLIDER
slider = CTkSlider(master=tabview.tab("Tab 3"), from_=0, to=100, number_of_steps=100, fg_color="black")
slider.place(relx=0.8, rely=0.7, anchor="center")

#ENTRY
entry = CTkEntry(frame, placeholder_text="Escribe algo...", fg_color="black", corner_radius=32)
entry.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



app.mainloop()