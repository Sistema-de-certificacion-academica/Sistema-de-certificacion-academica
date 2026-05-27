from app.plantillas.repository.plantillas_repo import template_repository
from app.plantillas.domain.plantillas import TemplateCreate

class TemplateService:

    def __init__(self):
        self.repo = template_repository

    def crear_plantilla(self, data: TemplateCreate) -> dict:
        existente = self.repo.get_activa_by_tipo(data.tipo_certificado)
        if existente:
            raise ValueError(f"Ya existe una plantilla activa para el tipo de certificado '{data.tipo_certificado}'")

        plantilla = self.repo.save(data)

        return {
            "success": True,
            "statusCode": 201,
            "message": "Plantilla creada correctamente",
            "data": {
                "id": plantilla.id,
                "nombre": plantilla.nombre,
                "tipo_certificado": plantilla.tipo_certificado,
                "estructura": plantilla.estructura,
                "activa": plantilla.activa
            }
        }

template_service = TemplateService()
