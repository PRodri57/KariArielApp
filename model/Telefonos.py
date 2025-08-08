from typing import Optional

class Telefono:
    CAMPOS_OBLIGATORIOS = ["marca", "modelo", "dni"]

    def __init__(self, telefono_id: Optional[int] = None, marca: str = None, modelo: str = None, contrasena: Optional[str] = None, comentario: Optional[str] = None, dni: Optional[int] = None):
        if not marca or not modelo or dni is None:
            raise ValueError("Marca, modelo y dni son obligatorios.")
        self.telefono_id = telefono_id
        self.marca = marca
        self.modelo = modelo
        self.contrasena = contrasena or ""
        self.comentario = comentario or ""
        self.dni = dni

    @classmethod
    def from_dict(cls, datos):
        return cls(
            telefono_id=datos.get("telefono_id"),
            marca=datos.get("marca"),
            modelo=datos.get("modelo"),
            contrasena=datos.get("contrasena"),
            comentario=datos.get("comentario"),
            dni=datos.get("dni"),
        )

    def to_dict(self):
        return {
            "telefono_id": self.telefono_id,
            "marca": self.marca,
            "modelo": self.modelo,
            "contrasena": self.contrasena,
            "comentario": self.comentario,
            "dni": self.dni,
        }
