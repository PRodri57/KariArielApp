def centrar_ventana(ventana, aplicacion_ancho, aplicacion_alto):
    """
    Centra la ventana en la pantalla.

    :param ventana: La ventana a centrar.
    :param aplicacion_ancho: Ancho de la aplicación.
    :param aplicacion_alto: Alto de la aplicación.
    """
    # Obtener el tamaño de la pantalla
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()

    # Calcular las coordenadas x e y para centrar la ventana
    x = (pantalla_ancho // 2) - (aplicacion_ancho // 2)
    y = (pantalla_alto // 2) - (aplicacion_alto // 2)

    # Establecer la posición de la ventana
    return ventana.geometry(f"{aplicacion_ancho}x{aplicacion_alto}+{x}+{y}")