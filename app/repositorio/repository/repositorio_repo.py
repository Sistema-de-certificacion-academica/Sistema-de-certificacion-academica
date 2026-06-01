from typing import Optional
from app.repositorio.domain.repositorio import CertificadoRepositorio


class RepositorioRepository:
    _certificados: list[CertificadoRepositorio] = []
    _seeded: bool = False

    def __init__(self):
        pass

    def get_by_uuid(self, uuid: str) -> Optional[CertificadoRepositorio]:
        for c in type(self)._certificados:
            if c.uuid == uuid:
                return c
        return None

    def get_by_usuario_id(self, usuario_id: int) -> list[CertificadoRepositorio]:
        return [c for c in type(self)._certificados if c.usuario_id == usuario_id]
    
    def actualizar_estado(self, uuid: str, nuevo_estado: str) -> Optional[CertificadoRepositorio]:
        certificado = self.get_by_uuid(uuid)
        if not certificado:
            return None
        certificado.estado = nuevo_estado
        return certificado


repositorio_repository = RepositorioRepository()
