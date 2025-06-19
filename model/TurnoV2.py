from datetime import datetime

class TurnoV2:
    """
    Modelo para representar un turno de reparación o servicio.
    """
    CAMPOS_OBLIGATORIOS = ["dni", "tipo_servicio", "fecha_ingreso"]

    def __init__(self, numero_orden=None, dni=None, tipo_servicio=None, tecnico=None, fecha_ingreso=None, descripcion=None, presupuesto=0.0, sena=0.0, sena_revision=0.0, garantia=0, fecha_reparacion=None, fecha_retiro=None, comentario_turno=None):
        if dni is None or tipo_servicio is None or fecha_ingreso is None:
            raise ValueError("DNI, tipo_servicio y fecha_ingreso son obligatorios.")

        self.numero_orden = numero_orden
        self.dni = str(dni)
        self.tipo_servicio = tipo_servicio
        self.tecnico = tecnico or ""
        self.fecha_ingreso = self._parse_fecha(fecha_ingreso)
        self.descripcion = descripcion or ""
        self.presupuesto = float(presupuesto) if presupuesto is not None else 0.0
        self.sena = float(sena) if sena is not None else 0.0
        self.sena_revision = float(sena_revision) if sena_revision is not None else 0.0
        self.garantia = int(garantia) if garantia is not None else 0
        self.fecha_reparacion = self._parse_fecha(fecha_reparacion)
        self.fecha_retiro = self._parse_fecha(fecha_retiro)
        self.comentario_turno = comentario_turno or ""

    @staticmethod
    def _parse_fecha(fecha):
        if fecha is None or fecha == "":
            return None
        if isinstance(fecha, datetime):
            return fecha
        if isinstance(fecha, str):
            for fmt in ("%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y"):
                try:
                    return datetime.strptime(fecha, fmt)
                except ValueError:
                    continue
        raise ValueError(f"Formato de fecha no válido: {fecha}")

    @classmethod
    def from_dict(cls, datos):
        """
        Crea una instancia de TurnoV2 a partir de un diccionario.
        """
        return cls(
            numero_orden=datos.get("numero_orden"),
            dni=datos.get("dni"),
            tipo_servicio=datos.get("servicio") or datos.get("tipo_servicio"),
            tecnico=datos.get("tecnico"),
            fecha_ingreso=datos.get("fecha_ingreso"),
            descripcion=datos.get("descripcion"),
            presupuesto=datos.get("presupuesto"),
            sena=datos.get("sena"),
            sena_revision=datos.get("sena_revision"),
            garantia=datos.get("garantia"),
            fecha_reparacion=datos.get("fecha_reparacion"),
            fecha_retiro=datos.get("fecha_retiro"),
            comentario_turno=datos.get("comentario") or datos.get("comentario_turno"),
        )

    def to_dict(self):
        """
        Convierte la instancia en un diccionario, útil para guardar en la base de datos.
        """
        return {
            "numero_orden": self.numero_orden,
            "dni": self.dni,
            "tipo_servicio": self.tipo_servicio,
            "tecnico": self.tecnico,
            "fecha_ingreso": self.fecha_ingreso.strftime("%Y-%m-%d") if self.fecha_ingreso else None,
            "descripcion": self.descripcion,
            "presupuesto": self.presupuesto,
            "sena": self.sena,
            "sena_revision": self.sena_revision,
            "garantia": self.garantia,
            "fecha_reparacion": self.fecha_reparacion.strftime("%Y-%m-%d") if self.fecha_reparacion else None,
            "fecha_retiro": self.fecha_retiro.strftime("%Y-%m-%d") if self.fecha_retiro else None,
            "comentario_turno": self.comentario_turno,
        }
        
