from pydantic import BaseModel, Field, field_validator
from datetime import datetime

ESTADOS_CERTIFICADO = frozenset({"DISPONIBLE", "ANULADO", "VIGENTE"})

class Certificado:
    def __init__(self, uuid: str, estudiante: str, tipo_certificado: str, fecha_emision: str,
                 estado: str = "DISPONIBLE", hash_archivo: str = None):
        self.uuid = uuid
        self.estudiante = estudiante
        self.tipo_certificado = tipo_certificado
        self.fecha_emision = fecha_emision
        self.estado = estado
        self.hash_archivo = hash_archivo

    def es_valido(self) -> bool:
        return self.estado == "DISPONIBLE"

    def esta_anulado(self) -> bool:
        return self.estado == "ANULADO"

class Verificacion:
    def __init__(self, id: int, uuid_consultado: str, ip_verificador: str):
        self.id = id
        self.uuid_consultado = uuid_consultado
        self.ip_verificador = ip_verificador
        self.timestamp = datetime.utcnow().isoformat() + "Z"

class VerificacionResponse(BaseModel):
    valido: bool
    uuid: str
    estudiante: str = None
    tipo_certificado: str = None
    fecha_emision: str = None
    estado: str = None