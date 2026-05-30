from app.plantillas.repository.plantillas_repo import PlantillaRepository, plantilla_repository
from app.plantillas.domain.plantillas import PlantillaCreate, PlantillaUpdate

TIPOS_CERTIFICADO_PERMITIDOS = {
    "CERTIFICADO_ESTUDIO",
    "CERTIFICADO_NOTAS",
    "CERTIFICADO_GRADUACION",
    "CERTIFICADO_CONDUCTA",
    "PAZ_Y_SALVO"
}

class TipoInvalidoError(ValueError):
    pass

class PlantillaUsadaError(Exception):
    pass

class PlantillaService:

    def __init__(self, repo: PlantillaRepository):
        self.repo = repo

    def _validar_tipo_certificado(self, tipo_certificado: str) -> None:
        if tipo_certificado not in TIPOS_CERTIFICADO_PERMITIDOS:
            raise TipoInvalidoError("El tipo de certificado no es válido")

    def crear_plantilla(self, data: PlantillaCreate) -> dict:
        self._validar_tipo_certificado(data.tipo_certificado)
        existente = self.repo.get_activa_by_tipo(data.tipo_certificado)
        if existente:
            raise ValueError(f"Ya existe una plantilla activa para el tipo '{data.tipo_certificado}'")
        plantilla = self.repo.save(data)
        return plantilla.to_response()

    def editar_plantilla(self, plantilla_id: int, data: PlantillaUpdate) -> dict:
        plantilla = self.repo.get_by_id(plantilla_id)
        if not plantilla:
            raise ValueError("No existe una plantilla con el id proporcionado")
        if self.repo.tiene_certificados(plantilla_id):
            raise PlantillaUsadaError("No se puede editar una plantilla que ya fue usada para generar certificados")
        if data.tipo_certificado is not None:
            self._validar_tipo_certificado(data.tipo_certificado)
        plantilla = self.repo.update(
            plantilla_id,
            nombre=data.nombre,
            tipo_certificado=data.tipo_certificado,
            estructura=data.estructura
        )
        return plantilla.to_response()

    def listar_plantillas(self) -> list:
        plantillas = self.repo.get_all()
        return [p.to_response_lista() for p in plantillas]

plantilla_service = PlantillaService(repo=plantilla_repository)