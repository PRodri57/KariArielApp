from typing import Optional

class Cliente:
    CAMPOS_OBLIGATORIOS = ["dni", "nombre_apellido"]

    def __init__(self, dni: str, nombre_apellido: str, telefono: Optional[str] = None, email: Optional[str] = None, direccion: Optional[str] = None):
        if not dni or not nombre_apellido:
            raise ValueError("DNI y nombre/apellido son obligatorios.")
        self.dni = str(dni)
        self.nombre_apellido = nombre_apellido
        self.telefono = telefono or ""
        self.email = email or ""
        self.direccion = direccion or ""

    @classmethod
    def from_dict(cls, datos):
        return cls(
            dni=datos.get("dni"),
            nombre_apellido=datos.get("nombre_apellido") or datos.get("nombre") or datos.get("nombre_apelllido"),
            telefono=datos.get("telefono"),
            email=datos.get("email"),
            direccion=datos.get("direccion"),
        )

    def to_dict(self):
        return {
            "dni": self.dni,
            "nombre_apellido": self.nombre_apellido,
            "telefono": self.telefono,
            "email": self.email,
            "direccion": self.direccion,
        }
        
    