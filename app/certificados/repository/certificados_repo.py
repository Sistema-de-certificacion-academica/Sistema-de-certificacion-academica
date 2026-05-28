from typing import Optional
from app.certificados.domain.certificados import Certificate, CertificateCreate

class CertificateRepository:
    _certificados: list[Certificate] = []
    _next_id: int = 1

    def save(self, data: CertificateCreate, uuid: str, fecha_emision: str, estado: str = "GENERADO") -> Certificate:
        certificado = Certificate(
            id=type(self)._next_id,
            uuid=uuid,
            solicitud_id=data.solicitud_id,
            plantilla_id=data.plantilla_id,
            estado=estado,
            fecha_emision=fecha_emision
        )
        self._certificados.append(certificado)
        type(self)._next_id += 1
        return certificado

    def get_by_uuid(self, uuid: str) -> Optional[Certificate]:
        for c in self._certificados:
            if c.uuid == uuid:
                return c
        return None

certificate_repository = CertificateRepository()
