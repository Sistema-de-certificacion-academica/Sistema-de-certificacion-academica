from fastapi import APIRouter, Depends, status
from app.core.dependencies import require_admin
from app.usuarios.domain.schemas import UserCreate, UserDeleteResponse, UserResponse, UserResponseData
from app.usuarios.services.usuario_service import UserService

router = APIRouter(prefix="/api/v1/usuarios", tags=["Usuarios"])
user_service = UserService()


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user_data: UserCreate,
    current_user: dict = Depends(require_admin),
):

    db_user = user_service.registrar_usuario(user_data)
    return UserResponse(
        success=True,
        statusCode=201,
        message="Usuario registrado correctamente",
        data=UserResponseData.model_validate(db_user),
    )


@router.delete("/{user_id}", response_model=UserDeleteResponse, status_code=status.HTTP_200_OK)
def delete_user(
    user_id: int,
    current_user: dict = Depends(require_admin),
):
    user_service.eliminar_usuario(user_id)
    return UserDeleteResponse(
        success=True,
        statusCode=200,
        message="Usuario eliminado correctamente",
    )
