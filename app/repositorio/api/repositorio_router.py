from fastapi import APIRouter, Depends, HTTPException, status
from app.core.dependencies import require_estudiante_o_admin
from app.repositorio.services.repositorio_service import repositorio_service

router = APIRouter(
    prefix="/api/v1/repositorio",
    tags=["Repositorio"]
)


@router.get("/certificados/{uuid}", status_code=status.HTTP_200_OK)
def buscar_certificado(
    uuid: str,
    current_user: dict = Depends(require_estudiante_o_admin)
):
    try:
        usuario_id = current_user.get("id")
        rol = current_user.get("rol")
        return repositorio_service.buscar_certificado_por_uuid(uuid, usuario_id, rol)
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
