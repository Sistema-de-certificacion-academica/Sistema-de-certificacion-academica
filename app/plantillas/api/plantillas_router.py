from fastapi import APIRouter, Depends, HTTPException, status
from app.core.dependencies import require_admin
from app.plantillas.domain.plantillas import PlantillaCreate, PlantillaUpdate
from app.plantillas.services.plantillas_service import plantilla_service

router = APIRouter(prefix="/api/v1/plantillas", tags=["Plantillas"])

@router.post("", status_code=status.HTTP_201_CREATED)
def crear_plantilla(data: PlantillaCreate, current_user: dict = Depends(require_admin)):
    try:
        return plantilla_service.crear_plantilla(data)
    except ValueError as e:
        mensaje = str(e)
        if "no es válido" in mensaje:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=mensaje
            )
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=mensaje
        )

@router.get("", status_code=status.HTTP_200_OK)
def listar_plantillas(current_user: dict = Depends(require_admin)):
    return plantilla_service.listar_plantillas()

@router.put("/{plantilla_id}", status_code=status.HTTP_200_OK)
def editar_plantilla(plantilla_id: int, data: PlantillaUpdate, current_user: dict = Depends(require_admin)):
    try:
        return plantilla_service.editar_plantilla(plantilla_id, data)
    except ValueError as e:
        mensaje = str(e)
        if "no existe" in mensaje:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=mensaje
            )
        if "no es válido" in mensaje:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=mensaje
            )
        if "no puede editarse" in mensaje:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=mensaje
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=mensaje
        )
