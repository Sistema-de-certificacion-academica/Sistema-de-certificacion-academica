import uuid
from app.repositorio.repository.repositorio_repo import repositorio_repository
from app.repositorio.domain.repositorio import ESTADOS_REPOSITORIO, CertificateRepositoryResponse, CertificateHistoryItem, CertificateMetadataResponse


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

    def obtener_historial_estudiante(self, estudiante_id: int, usuario_id: int, rol: str) -> dict:
        if rol == "ESTUDIANTE" and estudiante_id != usuario_id:
            raise PermissionError("No tiene permisos para consultar este historial")

        certificados = self.repo.get_by_usuario_id(estudiante_id)

        if not certificados:
            return {
                "success": True,
                "statusCode": 200,
                "message": "El estudiante no tiene certificados emitidos",
                "data": []
            }

        return {
            "success": True,
            "statusCode": 200,
            "message": "Historial de certificados encontrado",
            "data": [
                CertificateHistoryItem(
                    uuid=c.uuid,
                    certificado_id=c.certificado_id,
                    tipo_certificado=c.tipo_certificado,
                    fecha_emision=c.fecha_emision,
                    estado=c.estado
                ).model_dump()
                for c in certificados
            ]
        }


    def obtener_metadatos_publicos(self, uuid_str: str) -> dict:
        certificado = self.repo.get_by_uuid(uuid_str)

        if not certificado:
            raise ValueError("No existe un certificado con el UUID proporcionado")

        data = CertificateMetadataResponse(
            uuid=certificado.uuid,
            tipo_certificado=certificado.tipo_certificado,
            fecha_emision=certificado.fecha_emision,
            estado=certificado.estado
        )

        return {
            "success": True,
            "statusCode": 200,
            "message": "Metadatos del certificado encontrados",
            "data": data.model_dump()
        }


repositorio_service = RepositorioService()
