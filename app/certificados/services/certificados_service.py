from datetime import datetime, timezone
from uuid import uuid4
from app.certificados.domain.certificados import CertificateCreate
from app.certificados.repository.certificados_repo import CertificateRepository, certificate_repository
from app.plantillas.repository.plantillas_repo import plantilla_repository
from app.solicitudes.repository.solicitudes_repo import solicitud_repository
from app.repositorio.repository.repositorio_repo import repositorio_repository
from app.usuarios.repository.usuario_repo import usuario_repository 


class SolicitudNoAprobadaError(Exception):
    pass

class PlantillaInactivaError(Exception):
    pass

class CertificadoYaAnuladoError(Exception):
    pass


class CertificateService:

    def __init__(self, repo: CertificateRepository,
                 solicitud_repo, plantilla_repo,
                 repositorio_repo, usuario_repo):  
        self.repo = repo
        self.solicitud_repo = solicitud_repo
        self.plantilla_repo = plantilla_repo
        self.repositorio_repo = repositorio_repo
        self.usuario_repo = usuario_repo 

    def generar_certificado(self, data: CertificateCreate) -> dict:
        solicitud = self.solicitud_repo.get_by_id(data.solicitud_id)
        if not solicitud:
            raise ValueError("No existe una solicitud con el id proporcionado")
        if solicitud.estado != "APROBADA":
            raise SolicitudNoAprobadaError(
                "Solo se pueden generar certificados de solicitudes aprobadas"
            )

        plantilla = self.plantilla_repo.get_activa_by_tipo(solicitud.tipo_certificado)
        if not plantilla:
            raise ValueError(
                "No existe una plantilla activa para el tipo de certificado de esta solicitud"
            )

        usuario = self.usuario_repo.get_by_id(solicitud.usuario_id)
        if not usuario:
            raise ValueError("No existe el usuario asociado a esta solicitud")

        uuid_value = str(uuid4())
        while self.repo.obtener_por_uuid(uuid_value):
            uuid_value = str(uuid4())

        fecha_emision = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        ruta_pdf = f"/certificados/pdf/{uuid_value}.pdf"

        certificado = self.repo.crear(
            solicitud_id=data.solicitud_id,
            plantilla_id=plantilla.id,
            uuid=uuid_value,
            fecha_emision=fecha_emision,
            ruta_pdf=ruta_pdf,
            nombre_estudiante=usuario.nombre,
            programa_academico=usuario.programa_academico,  
        )

        self.repositorio_repo.crear(
        uuid=uuid_value,
        certificado_id=certificado.id,
        usuario_id=solicitud.usuario_id,
        tipo_certificado=solicitud.tipo_certificado,
        fecha_emision=fecha_emision,
        estado="GENERADO",
        ruta_archivo=ruta_pdf,
        )

        self.plantilla_repo.marcar_como_usada(plantilla.id)
        return certificado.to_response()

    def anular_certificado(self, certificado_id: int) -> dict:
        certificado = self.repo.obtener_por_id(certificado_id)
        if not certificado:
            raise ValueError("No existe un certificado con el id proporcionado")
        if certificado.esta_anulado():
            raise CertificadoYaAnuladoError("El certificado ya está anulado")

        certificado = self.repo.actualizar_estado(certificado_id, "ANULADO")
        self.repositorio_repo.actualizar_estado(certificado.uuid, "ANULADO")
        return certificado.to_anulado_response()


certificate_service = CertificateService(
    repo=certificate_repository,
    solicitud_repo=solicitud_repository,
    plantilla_repo=plantilla_repository,
    repositorio_repo=repositorio_repository,
    usuario_repo=usuario_repository,  
)