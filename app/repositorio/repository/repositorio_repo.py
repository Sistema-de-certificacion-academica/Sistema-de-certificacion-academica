from typing import Optional
from app.repositorio.domain.repositorio import CertificadoRepositorio


class RepositorioRepository:
    _certificados: list[CertificadoRepositorio] = []
    _seeded: bool = False

    def __init__(self):
        if not type(self)._seeded:
            self._seed()
            type(self)._seeded = True

    def _seed(self):
        data = [
            CertificadoRepositorio(
                uuid="550e8400-e29b-41d4-a716-446655440001",
                certificado_id=1,
                usuario_id=1,
                tipo_certificado="CERTIFICADO_ESTUDIO",
                fecha_emision="2026-03-18",
                estado="DISPONIBLE",
                ruta_archivo="/certificados/certificado_1.pdf"
            ),
            CertificadoRepositorio(
                uuid="550e8400-e29b-41d4-a716-446655440002",
                certificado_id=2,
                usuario_id=1,
                tipo_certificado="CERTIFICADO_ESTUDIO",
                fecha_emision="2026-04-10",
                estado="DISPONIBLE",
                ruta_archivo="/certificados/certificado_2.pdf"
            ),
            CertificadoRepositorio(
                uuid="550e8400-e29b-41d4-a716-446655440003",
                certificado_id=3,
                usuario_id=2,
                tipo_certificado="CERTIFICADO_ESTUDIO",
                fecha_emision="2026-05-01",
                estado="ANULADO",
                ruta_archivo="/certificados/certificado_3.pdf"
            ),
        ]
        type(self)._certificados.extend(data)

    def get_by_uuid(self, uuid: str) -> Optional[CertificadoRepositorio]:
        for c in type(self)._certificados:
            if c.uuid == uuid:
                return c
        return None

    def get_by_usuario_id(self, usuario_id: int) -> list[CertificadoRepositorio]:
        return [c for c in type(self)._certificados if c.usuario_id == usuario_id]


repositorio_repository = RepositorioRepository()
