from config.supabase_client import supabase

# ---------------------- TURNOS ----------------------
def crear_turno(data):
    try:
        respuesta = supabase.table('turnos_v2').insert(data).execute()
        print("Se creo el turno correctamente")
        return respuesta.data
    except Exception as e:
        print(f"Error al crear turno: {e}")
        return None

def obtener_turno(numero_orden):
    try:
        respuesta = supabase.table('turnos_v2').select('*').eq('numero_orden', numero_orden).execute()
        return respuesta.data
    except Exception as e:
        print(f"Error al obtener turno: {e}")
        return None

def actualizar_turno(numero_orden, data):
    try:
        respuesta = supabase.table('turnos_v2').update(data).eq('numero_orden', numero_orden).execute()
        return respuesta.data
    except Exception as e:
        print(f"Error al actualizar turno: {e}")
        return None

def eliminar_turno(numero_orden):
    try:
        respuesta = supabase.table('turnos_v2').delete().eq('numero_orden', numero_orden).execute()
        return respuesta.data
    except Exception as e:
        print(f"Error al eliminar turno: {e}")
        return None

def obtener_turnos_por_fecha(fecha):
    try:
        respuesta = supabase.table('turnos_v2').select('*').eq('fecha_ingreso', fecha).execute()
        return respuesta.data
    except Exception as e:
        print(f"Error al obtener turnos por fecha: {e}")
        return None

# ---------------------- CLIENTES ----------------------
def crear_cliente(data):
    try:
        respuesta = supabase.table('clientes').insert(data).execute()
        return respuesta.data
    except Exception as e:
        print(f"Error al crear cliente: {e}")
        return None

def obtener_cliente(dni_partial: str, limit: int = 5):
    try:
        respuesta = supabase.table('clientes').select('*').eq('dni', int(dni_partial)).limit(limit).execute()
        return respuesta.data
    except Exception as e:
        print(f"Error buscando clientes: {e}")
        return None

def actualizar_cliente(dni, data):
    try:
        respuesta = supabase.table('clientes').update(data).eq('dni', dni).execute()
        return respuesta.data
    except Exception as e:
        print(f"Error al actualizar cliente: {e}")
        return None

def eliminar_cliente(dni):
    try:
        respuesta = supabase.table('clientes').delete().eq('dni', dni).execute()
        return respuesta.data
    except Exception as e:
        print(f"Error al eliminar cliente: {e}")
        return None

# ---------------------- TELEFONOS ----------------------
def crear_telefono(data):
    try:
        respuesta = supabase.table('telefonos').insert(data).execute()
        return respuesta.data
    except Exception as e:
        print(f"Error al crear teléfono: {e}")
        return None

def obtener_telefono(telefono_id):
    try:
        respuesta = supabase.table('telefonos').select('*').eq('telefono_id', telefono_id).execute()
        return respuesta.data
    except Exception as e:
        print(f"Error al obtener teléfono: {e}")
        return None

def actualizar_telefono(telefono_id, data):
    try:
        respuesta = supabase.table('telefonos').update(data).eq('telefono_id', telefono_id).execute()
        return respuesta.data
    except Exception as e:
        print(f"Error al actualizar teléfono: {e}")
        return None

def eliminar_telefono(telefono_id):
    try:
        respuesta = supabase.table('telefonos').delete().eq('telefono_id', telefono_id).execute()
        return respuesta.data
    except Exception as e:
        print(f"Error al eliminar teléfono: {e}")
        return None

# ---------------------- HISTORIALES ----------------------
def crear_historial(data):
    try:
        respuesta = supabase.table('historiales').insert(data).execute()
        return respuesta.data
    except Exception as e:
        print(f"Error al crear historial: {e}")
        return None

def obtener_historial(historial_id):
    try:
        respuesta = supabase.table('historiales').select('*').eq('historial_id', historial_id).execute()
        return respuesta.data
    except Exception as e:
        print(f"Error al obtener historial: {e}")
        return None

def actualizar_historial(historial_id, data):
    try:
        respuesta = supabase.table('historiales').update(data).eq('historial_id', historial_id).execute()
        return respuesta.data
    except Exception as e:
        print(f"Error al actualizar historial: {e}")
        return None

def eliminar_historial(historial_id):
    try:
        respuesta = supabase.table('historiales').delete().eq('historial_id', historial_id).execute()
        return respuesta.data
    except Exception as e:
        print(f"Error al eliminar historial: {e}")
        return None 