from fastapi import APIRouter, Depends, HTTPException, status
from app.core.dependencies import require_estudiante
from app.solicitudes.domain.solicitudes import SolicitudCreate
from app.solicitudes.services.solicitudes_service import solicitud_service

router = APIRouter(
    prefix="/api/v1/solicitudes",
    tags=["Solicitudes"]
)

@router.post("", status_code=status.HTTP_201_CREATED)
def crear_solicitud(data: SolicitudCreate, current_user: dict = Depends(require_estudiante)):
    try:
        usuario_id = current_user.get("id")
        return solicitud_service.crear_solicitud(usuario_id, data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )