from typing import Optional
from app.plantillas.domain.plantillas import Plantilla, TemplateCreate

class TemplateRepository:
    _plantillas: list[Plantilla] = []
    _next_id: int = 1

    def save(self, data: TemplateCreate) -> Plantilla:
        plantilla = Plantilla(
            id=self._next_id,
            nombre=data.nombre,
            tipo_certificado=data.tipo_certificado,
            estructura=data.estructura,
            activa=True
        )
        self._plantillas.append(plantilla)
        type(self)._next_id += 1
        return plantilla

    def get_activa_by_tipo(self, tipo_certificado: str) -> Optional[Plantilla]:
        for p in self._plantillas:
            if p.tipo_certificado == tipo_certificado and p.activa:
                return p
        return None

template_repository = TemplateRepository()
