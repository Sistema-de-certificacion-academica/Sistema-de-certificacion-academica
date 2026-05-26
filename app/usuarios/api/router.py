from fastapi import APIRouter, Depends, HTTPException, status
from app.core.dependencies import require_admin
from app.usuarios.domain.usuarios import UserCreate
from app.usuarios.services.usuario_service import usuario_services, ConflictError

router = APIRouter(prefix="/api/v1/usuarios", tags=["Usuarios"])

@router.post("", status_code=status.HTTP_201_CREATED)
def registrar_usuario(user_data: UserCreate, current_user: dict = Depends(require_admin)):
    try:
        return usuario_services.registrar_usuario(user_data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

@router.post("/registro", status_code=status.HTTP_201_CREATED)
def registro_estudiante(user_data: UserCreate):
    try:
        return usuario_services.registrar_estudiante(user_data)
    except ValueError as e:
        if "solo acepta rol ESTUDIANTE" in str(e):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
def eliminar_usuario(user_id: int, current_user: dict = Depends(require_admin)):
    try:
        admin_id = current_user.get("id")
        return usuario_services.eliminar_usuario(user_id, admin_id)
    except ConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except ValueError as e:
        if "si mismo" in str(e):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))