from typing import Optional
from app.verificaciones.domain.verificaciones import Certificado, Verificacion

class VerificacionRepository:
    _certificados: list[Certificado] = []
    _verificaciones: list[Verificacion] = []
    _siguiente_id: int = 1

    def __init__(self):
        if not type(self)._certificados:
            self._seed()

    def _seed(self):
        """
        Certificados de prueba mientras el módulo
        de generación no esté listo.
        TODO: conectar con módulo de certificados.
        """
        import hashlib
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
            ),

            Certificado(
                uuid="770a1600-g41d-63f6-c938-668877662222",
                estudiante="Carlos Perez",
                tipo_certificado="CERTIFICADO_GRADUACION",
                fecha_emision="2026-01-15",
                estado="DISPONIBLE",
                hash_archivo="hash_alterado_diferente"  # simula documento alterado
            )
        ]

        type(self)._certificados.extend(certificados_prueba)

    def get_certificado_by_uuid(self, uuid: str) -> Optional[Certificado]:
        return next((c for c in self._certificados if c.uuid == uuid), None)

    def create_verificacion(self, uuid_consultado: str, ip_verificador: str) -> Verificacion:
        verificacion = Verificacion(id=type(self)._siguiente_id, uuid_consultado=uuid_consultado, ip_verificador=ip_verificador)
        type(self)._verificaciones.append(verificacion)
        type(self)._siguiente_id += 1
        return verificacion

    def get_verificaciones(self, uuid: str = None) -> list[Verificacion]:
        if uuid:
            return [v for v in self._verificaciones if v.uuid_consultado == uuid]
        return self._verificaciones.copy()

verificacion_repository = VerificacionRepository()