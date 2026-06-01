from typing import Optional
from app.repositorio.domain.repositorio import CertificadoRepositorio

class RepositorioRepository:
    _certificados: list[CertificadoRepositorio] = []

    def __init__(self):
        pass 

    def get_by_uuid(self, uuid: str) -> Optional[CertificadoRepositorio]:
        return next((c for c in type(self)._certificados if c.uuid == uuid), None)

    def get_by_usuario_id(self, usuario_id: int) -> list[CertificadoRepositorio]:
        return [c for c in type(self)._certificados if c.usuario_id == usuario_id]

    def crear(self, uuid: str, certificado_id: int, usuario_id: int, tipo_certificado: str, fecha_emision: str,
              estado: str, ruta_archivo: str) -> CertificadoRepositorio:
        registro = CertificadoRepositorio(
            uuid=uuid,
            certificado_id=certificado_id,
            usuario_id=usuario_id,
            tipo_certificado=tipo_certificado,
            fecha_emision=fecha_emision,
            estado=estado,
            ruta_archivo=ruta_archivo,
        )
        type(self)._certificados.append(registro)
        return registro

    def actualizar_estado(self, uuid: str, nuevo_estado: str) -> Optional[CertificadoRepositorio]:
        certificado = self.get_by_uuid(uuid)
        if not certificado:
            return None
        certificado.estado = nuevo_estado
        return certificado

repositorio_repository = RepositorioRepository()