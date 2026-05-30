from fastapi import APIRouter, Depends, HTTPException, status
from app.core.dependencies import require_estudiante
from app.solicitudes.domain.solicitudes import SolicitudCreate
from app.solicitudes.services.solicitudes_service import solicitud_service
from app.core.dependencies import require_estudiante, require_estudiante_o_admin, require_admin
from app.solicitudes.services.solicitudes_service import solicitud_service, ConflictError
from app.solicitudes.domain.solicitudes import SolicitudCreate, ActualizarEstadoRequest
from typing import Optional

router = APIRouter(prefix="/api/v1/solicitudes", tags=["Solicitudes"])

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
    
@router.get("/{solicitud_id}", status_code=status.HTTP_200_OK)
def consultar_solicitud(solicitud_id: int, current_user: dict = Depends(require_estudiante_o_admin)):
    try:
        usuario_id = current_user.get("id")
        rol = current_user.get("rol")
        return solicitud_service.consultar_solicitud(solicitud_id, usuario_id, rol)
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    
@router.delete("/{solicitud_id}", status_code=status.HTTP_200_OK)
def cancelar_solicitud(solicitud_id: int, current_user: dict = Depends(require_estudiante)):
    try:
        usuario_id = current_user.get("id")
        return solicitud_service.cancelar_solicitud(solicitud_id, usuario_id)
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=str(e))
    except ConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=str(e))
    
from app.solicitudes.domain.solicitudes import (
    SolicitudCreate, ActualizarEstadoRequest
)

@router.put("/{solicitud_id}/estado", status_code=status.HTTP_200_OK)
def aprobar_rechazar_solicitud(solicitud_id: int, data: ActualizarEstadoRequest, current_user: dict = Depends(require_admin)):
    try:
        return solicitud_service.aprobar_rechazar_solicitud(solicitud_id, data)
    except ConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("", status_code=status.HTTP_200_OK)
def listar_solicitudes(estado: Optional[str] = None, current_user: dict = Depends(require_admin)):
    try:
        return solicitud_service.listar_solicitudes(estado)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))