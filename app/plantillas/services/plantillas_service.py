from app.plantillas.repository.plantillas_repo import plantilla_repository
from app.plantillas.domain.plantillas import PlantillaCreate, PlantillaUpdate

# Tipos de certificados permitidos por la institución
TIPOS_CERTIFICADO_PERMITIDOS = {
    "CERTIFICADO_ESTUDIO",
    "CERTIFICADO_NOTAS",
    "CERTIFICADO_GRADUACION",
    "CERTIFICADO_CONDUCTA",
    "PAZ_Y_SALVO"
}

class PlantillaService:

    def __init__(self):
        self.repo = plantilla_repository

    def _validar_tipo_certificado(self, tipo_certificado: str) -> None:
        """Valida que el tipo de certificado sea permitido."""
        if tipo_certificado not in TIPOS_CERTIFICADO_PERMITIDOS:
            raise ValueError("El tipo de certificado no es válido")

    def crear_plantilla(self, data: PlantillaCreate) -> dict:
        self._validar_tipo_certificado(data.tipo_certificado)
        
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

    def editar_plantilla(self, plantilla_id: int, data: PlantillaUpdate) -> dict:
        plantilla = self.repo.get_by_id(plantilla_id)
        if not plantilla:
            raise ValueError("La plantilla no existe")

        if self.repo.tiene_certificados(plantilla_id):
            raise ValueError("La plantilla no puede editarse porque ya fue usada")

        if data.tipo_certificado is not None:
            self._validar_tipo_certificado(data.tipo_certificado)

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
            "message": "Plantillas encontradas",
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

plantilla_service = PlantillaService()
