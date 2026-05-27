from typing import Optional
from app.verificaciones.domain.verificaciones import Certificado
import hashlib

class VerificacionRepository:
    _certificados: list[Certificado] = []

    def __init__(self):
        if not self._certificados:
            self._seed()

    def _seed(self):
        certificados_prueba = [
            Certificado(
                uuid="550e8400-e29b-41d4-a716-446655440000",
                estudiante="Erick Gutierrez",
                tipo_certificado="CERTIFICADO_ESTUDIO",
                fecha_emision="2026-03-18",
                estado="DISPONIBLE",
                hash_archivo=hashlib.sha256(
                    b"certificado_erick"
                ).hexdigest()
            ),
            Certificado(
                uuid="660f9500-f30c-52e5-b827-557766551111",
                estudiante="Hansel Rodriguez",
                tipo_certificado="CERTIFICADO_NOTAS",
                fecha_emision="2026-02-10",
                estado="ANULADO",
                hash_archivo=hashlib.sha256(
                    b"certificado_hansel"
                ).hexdigest()
            )
        ]
        type(self)._certificados.extend(certificados_prueba)

    def get_by_uuid(self, uuid: str) -> Optional[Certificado]:
        return next((c for c in self._certificados if c.uuid == uuid), None)

    def get_all(self) -> list[Certificado]:
        return self._certificados.copy()

verificacion_repository = VerificacionRepository()