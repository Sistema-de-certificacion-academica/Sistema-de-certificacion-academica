from pydantic import BaseModel
from typing import Optional


ESTADOS_REPOSITORIO = frozenset({"DISPONIBLE", "ANULADO"})


class CertificadoRepositorio:
    def __init__(self, uuid: str, certificado_id: int, usuario_id: int,
                 fecha_emision: str, estado: str, ruta_archivo: str):
        self.uuid = uuid
        self.certificado_id = certificado_id
        self.usuario_id = usuario_id
        self.fecha_emision = fecha_emision
        self.estado = estado
        self.ruta_archivo = ruta_archivo


class CertificateRepositoryResponse(BaseModel):
    uuid: str
    certificado_id: int
    fecha_emision: str
    estado: str
    ruta_archivo: str
