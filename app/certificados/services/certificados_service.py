from datetime import datetime
from uuid import uuid4
from app.certificados.repository.certificados_repo import certificate_repository
from app.certificados.domain.certificados import CertificateCreate
from app.solicitudes.repository.solicitudes_repo import solicitud_repository
from app.plantillas.repository.plantillas_repo import plantilla_repository

class CertificateService:

    def __init__(self):
        self.repo = certificate_repository

    def generar_certificado(self, data: CertificateCreate) -> dict:
        solicitud = solicitud_repository.get_by_id(data.solicitud_id)
        if not solicitud:
            raise ValueError("No existe una solicitud con el id proporcionado")
        if solicitud.estado != "APROBADA":
            raise ValueError("La solicitud no está aprobada")

        plantilla = plantilla_repository.get_by_id(data.plantilla_id)
        if not plantilla:
            raise ValueError("No existe una plantilla con el id proporcionado")
        if not plantilla.activa:
            raise ValueError("La plantilla no está activa")

        uuid_value = str(uuid4())
        while self.repo.get_by_uuid(uuid_value):
            uuid_value = str(uuid4())

        fecha_emision = datetime.utcnow().isoformat() + "Z"
        certificado = self.repo.save(data, uuid_value, fecha_emision)

        plantilla_repository.marcar_como_usada(data.plantilla_id)

        return {
            "success": True,
            "statusCode": 201,
            "message": "Certificado generado correctamente",
            "data": {
                "id": certificado.id,
                "uuid": certificado.uuid,
                "solicitud_id": certificado.solicitud_id,
                "plantilla_id": certificado.plantilla_id,
                "estado": certificado.estado,
                "fecha_emision": certificado.fecha_emision,
                "ruta_pdf": certificado.ruta_pdf
            }
        }

certificate_service = CertificateService()
