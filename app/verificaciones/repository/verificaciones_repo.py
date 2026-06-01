import hashlib
from typing import Optional
from app.verificaciones.domain.verificaciones import CertificadoVerificacion, Verificacion

class VerificacionRepository:
    _certificados: list[CertificadoVerificacion] = []
    _verificaciones: list[Verificacion] = []
    _siguiente_id: int = 1
    _seeded: bool = False

    def __init__(self):
        if not type(self)._seeded:
            self._seed()
            type(self)._seeded = True

    def _seed(self):
        """
        Datos de prueba 
        El tercer certificado tiene hash alterado para probar caso 2.
        """
        certificados_prueba = [
            CertificadoVerificacion(
                uuid="550e8400-e29b-41d4-a716-446655440000",
                estudiante="Erick Gutierrez",
                tipo_certificado="CERTIFICADO_ESTUDIO",
                fecha_emision="2026-03-18",
                estado="DISPONIBLE",
                hash_archivo=hashlib.sha256(b"certificado_erick").hexdigest(),
            ),
            CertificadoVerificacion(
                uuid="660f9500-f30c-52e5-b827-557766551111",
                estudiante="Hansel Rodriguez",
                tipo_certificado="CERTIFICADO_NOTAS",
                fecha_emision="2026-02-10",
                estado="ANULADO",
                hash_archivo=hashlib.sha256(b"certificado_hansel").hexdigest(),
            ),
            CertificadoVerificacion(
                uuid="770a1600-a41d-63f6-c938-668877662222",
                estudiante="Carlos Perez",
                tipo_certificado="CERTIFICADO_GRADUACION",
                fecha_emision="2026-01-15",
                estado="DISPONIBLE",
                hash_archivo="hash_alterado_diferente",  # simula documento alterado
            ),
        ]
        type(self)._certificados.extend(certificados_prueba)

    def get_certificado_by_uuid(self, uuid: str) -> Optional[CertificadoVerificacion]:
        return next((c for c in type(self)._certificados if c.uuid == uuid), None)

    def registrar_verificacion(self, uuid_consultado: str, ip_verificador: str) -> Verificacion:
        verificacion = Verificacion(id=type(self)._siguiente_id, uuid_consultado=uuid_consultado, ip_verificador=ip_verificador)
        type(self)._verificaciones.append(verificacion)
        type(self)._siguiente_id += 1
        return verificacion

    def get_verificaciones(self, uuid: str = None) -> list[Verificacion]:
        if uuid:
            return [v for v in type(self)._verificaciones
                    if v.uuid_consultado == uuid]
        return type(self)._verificaciones.copy()

    def sincronizar_certificado(self, uuid: str, estudiante: str, tipo_certificado: str, fecha_emision: str, 
                                estado: str, hash_archivo: str) -> None:
        existente = self.get_certificado_by_uuid(uuid)
        if existente:
            existente.estado = estado
            existente.hash_archivo = hash_archivo
            return
        type(self)._certificados.append(CertificadoVerificacion(
            uuid=uuid,
            estudiante=estudiante,
            tipo_certificado=tipo_certificado,
            fecha_emision=fecha_emision,
            estado=estado,
            hash_archivo=hash_archivo,
        ))

verificacion_repository = VerificacionRepository()