from fastapi import APIRouter, Depends, HTTPException, status
from app.core.dependencies import require_admin
from app.plantillas.domain.plantillas import TemplateCreate, TemplateUpdate
from app.plantillas.services.plantillas_service import template_service

router = APIRouter(prefix="/api/v1/plantillas", tags=["Plantillas"])

@router.post("", status_code=status.HTTP_201_CREATED)
def crear_plantilla(data: TemplateCreate, current_user: dict = Depends(require_admin)):
    try:
        return template_service.crear_plantilla(data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )

@router.put("/{plantilla_id}", status_code=status.HTTP_200_OK)
def editar_plantilla(plantilla_id: int, data: TemplateUpdate, current_user: dict = Depends(require_admin)):
    try:
        return template_service.editar_plantilla(plantilla_id, data)
    except ValueError as e:
        mensaje = str(e)
        if "no puede editarse" in mensaje:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=mensaje
            )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=mensaje
        )
