import customtkinter as ctk
from PIL import ImageTk, Image

def leer_imagen(path, size):
    return ctk.CTkImage(Image.open(path), size=size)