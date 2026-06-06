from typing import Optional
from uuid import uuid4
from app.certificados.domain.certificados import Certificate

class CertificateRepository:
    _certificados: list[Certificate] = []
    _next_id: int = 1
    _seeded: bool = False

    def __init__(self):
        pass

    def obtener_todos(self) -> list[Certificate]:
        return self._certificados.copy()

    def obtener_por_id(self, id: int) -> Optional[Certificate]:
        return next((c for c in self._certificados if c.id == id), None)

    def obtener_por_uuid(self, uuid: str) -> Optional[Certificate]:
        return next((c for c in self._certificados if c.uuid == uuid), None)

    def crear(self, solicitud_id: int, plantilla_id: int, uuid: str, fecha_emision: str, estado: str = "GENERADO",
              ruta_pdf: str = None, nombre_estudiante: str = None) -> Certificate:
        certificado = Certificate(
            id=type(self)._next_id,
            uuid=uuid,
            solicitud_id=solicitud_id,
            plantilla_id=plantilla_id,
            estado=estado,
            fecha_emision=fecha_emision,
            ruta_pdf=ruta_pdf,
            nombre_estudiante=nombre_estudiante,   
        )
        type(self)._certificados.append(certificado)
        type(self)._next_id += 1
        return certificado

    def actualizar_estado(self, id: int, nuevo_estado: str) -> Optional[Certificate]:
        certificado = self.obtener_por_id(id)
        if not certificado:
            return None
        certificado.estado = nuevo_estado
        return certificado

certificate_repository = CertificateRepository()