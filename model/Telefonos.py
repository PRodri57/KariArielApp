from typing import Optional

class Telefono:
    CAMPOS_OBLIGATORIOS = ["marca", "modelo", "cliente_id"]

    def __init__(self, telefono_id: Optional[int] = None, marca: str = None, modelo: str = None, contrasena: Optional[str] = None, comentario: Optional[str] = None, cliente_id: Optional[int] = None):
        if not marca or not modelo or cliente_id is None:
            raise ValueError("Marca, modelo y cliente_id son obligatorios.")
        self.telefono_id = telefono_id
        self.marca = marca
        self.modelo = modelo
        self.contrasena = contrasena or ""
        self.comentario = comentario or ""
        self.cliente_id = cliente_id

    @classmethod
    def from_dict(cls, datos):
        return cls(
            telefono_id=datos.get("telefono_id"),
            marca=datos.get("marca"),
            modelo=datos.get("modelo"),
            contrasena=datos.get("contrasena"),
            comentario=datos.get("comentario"),
            cliente_id=datos.get("cliente_id"),
        )

    def to_dict(self):
        return {
            "telefono_id": self.telefono_id,
            "marca": self.marca,
            "modelo": self.modelo,
            "contrasena": self.contrasena,
            "comentario": self.comentario,
            "cliente_id": self.cliente_id,
        }
