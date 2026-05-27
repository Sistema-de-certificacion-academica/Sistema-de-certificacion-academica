from fastapi import APIRouter, Depends, HTTPException, status
from app.core.dependencies import require_admin
from app.plantillas.domain.plantillas import TemplateCreate
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
