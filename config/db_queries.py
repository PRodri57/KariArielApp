from config.supabase_client import supabase
from model.Telefonos import Telefono

# ---------------------- TURNOS ----------------------
def crear_turno(data):
    try:
        # Extraer información del teléfono del turno
        telefono_texto = data.get("telefono_texto", "")
        dni = data.get("dni")
        nombre_cliente = data.get("nombre", "")
        
        # Primero verificar si el cliente existe
        cliente_existente = buscar_clientes_por_dni(dni)
        if not cliente_existente or len(cliente_existente) == 0:
            # Crear el cliente si no existe
            print(f"Cliente con DNI {dni} no existe, creándolo...")
            cliente_data = {
                "dni": dni,
                "nombre_apellido": nombre_cliente,
                "telefono": telefono_texto,
                "email": "",
                "direccion": ""
            }
            cliente_result = crear_cliente(cliente_data)
            if not cliente_result:
                print("Error: No se pudo crear el cliente")
                return None
            print(f"Cliente creado exitosamente")
        
        # Buscar teléfonos existentes para este DNI
        telefonos_existentes = obtener_telefonos_por_dni(dni)
        telefono_id = None
        
        if telefonos_existentes and len(telefonos_existentes) > 0:
            # Usar el primer teléfono existente
            telefono_id = telefonos_existentes[0].get("telefono_id")
            print(f"Usando teléfono existente con ID: {telefono_id}")
        else:
            # Crear automáticamente un registro en la tabla telefonos usando el modelo
            telefono = Telefono(
                marca="No especificada",
                modelo="No especificado", 
                contrasena="",
                comentario=f"Teléfono: {telefono_texto}",
                dni=dni
            )
            
            # Crear el teléfono y obtener el telefono_id generado
            telefono_result = crear_telefono_con_modelo(telefono)
            if telefono_result and len(telefono_result) > 0:
                telefono_id = telefono_result[0].get("telefono_id")
                print(f"Teléfono creado con ID: {telefono_id}")
            else:
                print("Error: No se pudo crear el registro de teléfono")
                return None
        
        # Asignar el telefono_id al turno
        data["telefono_id"] = telefono_id
        
        # Remover el campo telefono_texto que no pertenece a la tabla turnos_v2
        if "telefono_texto" in data:
            del data["telefono_texto"]
        
        # Mapear comentario a comentario_turno si existe
        if "comentario" in data:
            data["comentario_turno"] = data["comentario"]
            del data["comentario"]
        
        # Mapear servicio a tipo_servicio si existe
        if "servicio" in data:
            data["tipo_servicio"] = data["servicio"]
            del data["servicio"]
        
        # Remover campos que no pertenecen a la tabla turnos_v2
        campos_a_remover = ["nombre", "cliente_info"]
        for campo in campos_a_remover:
            if campo in data:
                del data[campo]
        
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

def obtener_todos_los_clientes():
    try:
        respuesta = supabase.table('clientes').select('*').execute()
        return respuesta.data
    except Exception as e:
        print(f"Error obteniendo todos los clientes: {e}")
        return None

def buscar_clientes_por_dni(dni_partial: int, limit: int = 10):
    """Busca clientes por DNI parcial (search-as-you-type)"""
    try:
        if dni_partial is None or dni_partial < 0:
            return []
        
        # Para búsqueda parcial con int8, usamos búsqueda por rango
        # Si ingresamos "123", buscamos DNIs >= 123
        respuesta = supabase.table('clientes').select('*').gte('dni', dni_partial).limit(limit).execute()
        
        # Filtrar resultados para que empiecen exactamente con el número ingresado
        resultados_filtrados = []
        dni_str = str(dni_partial)
        
        for cliente in respuesta.data:
            cliente_dni_str = str(cliente['dni'])
            if cliente_dni_str.startswith(dni_str):
                resultados_filtrados.append(cliente)
        
        return resultados_filtrados
            
    except Exception as e:
        print(f"Error buscando clientes por DNI: {e}")
        return []

def obtener_cliente_por_dni(dni: int):
    """Obtiene un cliente específico por DNI"""
    try:
        respuesta = supabase.table('clientes').select('*').eq('dni', dni).execute()
        return respuesta.data
    except Exception as e:
        print(f"Error al obtener cliente por DNI: {e}")
        return None



def actualizar_cliente(dni: int, data):
    try:
        respuesta = supabase.table('clientes').update(data).eq('dni', dni).execute()
        return respuesta.data
    except Exception as e:
        print(f"Error al actualizar cliente: {e}")
        return None

def eliminar_cliente(dni: int):
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

def crear_telefono_con_modelo(telefono: Telefono):
    """Crea un teléfono usando el modelo Telefono"""
    try:
        datos = telefono.to_dict()
        # Remover telefono_id si es None para que se auto-genere
        if datos.get("telefono_id") is None:
            del datos["telefono_id"]
        
        respuesta = supabase.table('telefonos').insert(datos).execute()
        return respuesta.data
    except Exception as e:
        print(f"Error al crear teléfono con modelo: {e}")
        return None

def obtener_telefonos_por_dni(dni: int):
    """Busca teléfonos existentes por DNI del cliente"""
    try:
        respuesta = supabase.table('telefonos').select('*').eq('dni', dni).execute()
        return respuesta.data
    except Exception as e:
        print(f"Error al obtener teléfonos por DNI: {e}")
        return None

def obtener_telefono(telefono_id):
    try:
        respuesta = supabase.table('telefonos').select('*').eq('telefono_id', telefono_id).execute()
        return respuesta.data
    except Exception as e:
        print(f"Error al obtener teléfono: {e}")
        return None

def obtener_todos_los_telefonos():
    """Devuelve todos los teléfonos con su DNI asociado."""
    try:
        respuesta = supabase.table('telefonos').select('*').order('created_at', desc=True).execute()
        return respuesta.data
    except Exception as e:
        print(f"Error al obtener todos los teléfonos: {e}")
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