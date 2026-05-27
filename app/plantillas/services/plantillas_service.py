from app.plantillas.repository.plantillas_repo import template_repository
from app.plantillas.domain.plantillas import TemplateCreate, TemplateUpdate

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

    def editar_plantilla(self, plantilla_id: int, data: TemplateUpdate) -> dict:
        plantilla = self.repo.get_by_id(plantilla_id)
        if not plantilla:
            raise ValueError("No existe una plantilla con el id proporcionado")

        if self.repo.tiene_certificados(plantilla_id):
            raise ValueError("La plantilla no puede editarse porque ya fue usada")

        plantilla = self.repo.update(
            plantilla_id,
            nombre=data.nombre,
            tipo_certificado=data.tipo_certificado,
            estructura=data.estructura
        )

        return {
            "success": True,
            "statusCode": 200,
            "message": "Plantilla actualizada correctamente",
            "data": {
                "id": plantilla.id,
                "nombre": plantilla.nombre,
                "tipo_certificado": plantilla.tipo_certificado,
                "estructura": plantilla.estructura,
                "activa": plantilla.activa
            }
        }

    def listar_plantillas(self) -> dict:
        plantillas = self.repo.get_all()
        if not plantillas:
            return {
                "success": True,
                "statusCode": 200,
                "message": "No hay plantillas registradas",
                "data": []
            }
        return {
            "success": True,
            "statusCode": 200,
            "message": "Lista de plantillas obtenida",
            "data": [
                {
                    "id": p.id,
                    "nombre": p.nombre,
                    "tipo_certificado": p.tipo_certificado,
                    "activa": p.activa
                }
                for p in plantillas
            ]
        }

template_service = TemplateService()
