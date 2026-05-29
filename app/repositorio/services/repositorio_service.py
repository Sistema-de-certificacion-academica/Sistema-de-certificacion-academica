from app.repositorio.repository.repositorio_repo import repositorio_repository
from app.repositorio.domain.repositorio import ESTADOS_REPOSITORIO, CertificateRepositoryResponse


class RepositorioService:

    def __init__(self):
        self.repo = repositorio_repository

    def buscar_certificado_por_uuid(self, uuid: str, usuario_id: int, rol: str) -> dict:
        certificado = self.repo.get_by_uuid(uuid)

        if not certificado:
            raise ValueError("No existe un certificado con el UUID proporcionado")

        if rol == "ESTUDIANTE" and certificado.usuario_id != usuario_id:
            raise PermissionError("No tiene permisos para consultar este certificado")

        if certificado.estado not in ESTADOS_REPOSITORIO:
            raise RuntimeError(f"Estado de certificado inválido: {certificado.estado}")

        data = CertificateRepositoryResponse(
            uuid=certificado.uuid,
            certificado_id=certificado.certificado_id,
            fecha_emision=certificado.fecha_emision,
            estado=certificado.estado,
            ruta_archivo=certificado.ruta_archivo
        )

        return {
            "success": True,
            "statusCode": 200,
            "message": "Certificado encontrado",
            "data": data.model_dump()
        }


repositorio_service = RepositorioService()
