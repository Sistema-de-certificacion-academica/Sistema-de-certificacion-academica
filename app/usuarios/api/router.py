from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.dependencies import get_db, require_admin
from app.usuarios.domain.schemas import UserCreate, UserResponse, UserResponseData
from app.usuarios.services.usuario_service import UserService

router = APIRouter(prefix="/api/v1/usuarios", tags=["Usuarios"])
user_service = UserService()


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin),
):

    db_user = user_service.registrar_usuario(db, user_data)
    return UserResponse(
        success=True,
        statusCode=201,
        message="Usuario registrado correctamente",
        data=UserResponseData.model_validate(db_user),
    )
