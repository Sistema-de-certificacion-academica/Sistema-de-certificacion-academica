from datetime import datetime, timezone
from uuid import uuid4
from app.certificados.domain.certificados import CertificateCreate
from app.certificados.repository.certificados_repo import CertificateRepository, certificate_repository
from app.plantillas.repository.plantillas_repo import plantilla_repository
from app.solicitudes.repository.solicitudes_repo import solicitud_repository

class SolicitudNoAprobadaError(Exception):
    pass

class PlantillaInactivaError(Exception):
    pass

class CertificadoYaAnuladoError(Exception):
    pass

class CertificateService:

    def __init__(self, repo: CertificateRepository, solicitud_repo, plantilla_repo):
        self.repo = repo
        self.solicitud_repo = solicitud_repo
        self.plantilla_repo = plantilla_repo

    def generar_certificado(self, data: CertificateCreate) -> dict:
        solicitud = self.solicitud_repo.get_by_id(data.solicitud_id)
        if not solicitud:
            raise ValueError("No existe una solicitud con el id proporcionado")
        if solicitud.estado != "APROBADA":
            raise SolicitudNoAprobadaError("Solo se pueden generar certificados de solicitudes aprobadas")

        plantilla = self.plantilla_repo.get_by_id(data.plantilla_id)
        if not plantilla:
            raise ValueError("No existe una plantilla con el id proporcionado")
        if not plantilla.activa:
            raise PlantillaInactivaError("La plantilla seleccionada no está activa")

        uuid_value = str(uuid4())
        while self.repo.obtener_por_uuid(uuid_value):
            uuid_value = str(uuid4())

        fecha_emision = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        certificado = self.repo.crear(
            solicitud_id=data.solicitud_id,
            plantilla_id=data.plantilla_id,
            uuid=uuid_value,
            fecha_emision=fecha_emision,
        )

        self.plantilla_repo.marcar_como_usada(data.plantilla_id)
        return certificado.to_response()

    def anular_certificado(self, certificado_id: int, nuevo_estado: str) -> dict:
        certificado = self.repo.obtener_por_id(certificado_id)
        if not certificado:
            raise ValueError("No existe un certificado con el id proporcionado")
        if certificado.esta_anulado():
            raise CertificadoYaAnuladoError("El certificado ya está anulado")
        certificado = self.repo.actualizar_estado(certificado_id, nuevo_estado)
        return certificado.to_anulado_response()

certificate_service = CertificateService(
    repo=certificate_repository,
    solicitud_repo=solicitud_repository,
    plantilla_repo=plantilla_repository,
)