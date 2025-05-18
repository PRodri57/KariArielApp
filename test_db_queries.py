from config.db_queries import crear_turno, obtener_turno, actualizar_turno, eliminar_turno

# Prueba de creación
nuevo_turno = {
    "numero_orden": 1,
    "dni": 11222333,
    "telefono_id": 1,
    "tipo_servicio": "Reparación",
    "tecnico": "Juan",
    "fecha_ingreso": "2024-06-01",
    "descripcion": "Pantalla rota",
    "presupuesto": 5000,
    "sena": 1000,
    "sena_revision": 0,
    "garantia": 0,
    "fecha_reparacion": None,
    "fecha_retiro": None,
    "comentario_turno": "",
    "created_at": "2024-06-01T12:00:00"
}
print("Crear turno:", crear_turno(nuevo_turno))

# Prueba de obtención
print("Obtener turno:", obtener_turno(1))

# Prueba de actualización
print("Actualizar turno:", actualizar_turno(1, {"tecnico": "Ariel"}))

# Prueba de eliminación
print("Eliminar turno:", eliminar_turno(1))
