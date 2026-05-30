from typing import Optional
from app.plantillas.domain.plantillas import Plantilla, PlantillaCreate

class PlantillaRepository:
    _plantillas: list[Plantilla] = []
    _next_id: int = 1
    _ids_con_certificados: set[int] = set()

    def save(self, data: PlantillaCreate) -> Plantilla:
        plantilla = Plantilla(
            id=type(self)._next_id,
            nombre=data.nombre,
            tipo_certificado=data.tipo_certificado,
            estructura=data.estructura,
            activa=True
        )
        self._plantillas.append(plantilla)
        type(self)._next_id += 1
        return plantilla

    def get_by_id(self, plantilla_id: int) -> Optional[Plantilla]:
        for p in self._plantillas:
            if p.id == plantilla_id:
                return p
        return None

    def get_activa_by_tipo(self, tipo_certificado: str) -> Optional[Plantilla]:
        for p in self._plantillas:
            if p.tipo_certificado == tipo_certificado and p.activa:
                return p
        return None

    def update(self, plantilla_id: int, nombre: str = None,
               tipo_certificado: str = None, estructura: list = None) -> Plantilla:
        plantilla = self.get_by_id(plantilla_id)
        if nombre is not None:
            plantilla.nombre = nombre
        if tipo_certificado is not None:
            plantilla.tipo_certificado = tipo_certificado
        if estructura is not None:
            plantilla.estructura = estructura
        return plantilla

    def tiene_certificados(self, plantilla_id: int) -> bool:
        return plantilla_id in self._ids_con_certificados

    def get_all(self) -> list[Plantilla]:
        return self._plantillas.copy()

    def marcar_como_usada(self, plantilla_id: int):
        self._ids_con_certificados.add(plantilla_id)

plantilla_repository = PlantillaRepository()