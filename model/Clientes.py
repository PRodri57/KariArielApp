from typing import Optional

class Cliente:
    CAMPOS_OBLIGATORIOS = ["dni"]

    def __init__(self, dni: int, nombre_apellido: str, telefono: Optional[str] = None, email: Optional[str] = None, direccion: Optional[str] = None):
        if not dni:
            raise ValueError("DNI es obligatorio.")
        self.dni = int(dni)  # Mantener como int
        self.nombre_apellido = nombre_apellido or "Sin nombre"
        self.telefono = telefono or ""
        self.email = email or ""
        self.direccion = direccion or ""

    @classmethod
    def from_dict(cls, datos):
        # Obtener DNI como int desde la BD
        dni = datos.get("dni")
        if dni is not None:
            dni = int(dni)
        
        return cls(
            dni=dni,
            nombre_apellido=datos.get("nombre_apellido") or datos.get("nombre") or datos.get("nombre_apelllido"),
            telefono=datos.get("telefono"),
            email=datos.get("email"),
            direccion=datos.get("direccion"),
        )

    def to_dict(self):
        return {
            "dni": self.dni,  # Ya es int
            "nombre_apellido": self.nombre_apellido,
            "telefono": self.telefono,
            "email": self.email,
            "direccion": self.direccion,
        }
        
    