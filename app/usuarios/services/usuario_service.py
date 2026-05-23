from fastapi import HTTPException, status
from app.usuarios.repository.usuario_repo import UserRepository
from app.usuarios.domain.schemas import ROLES_PERMITIDOS, UserCreate
from app.core.security import hash_password

class UserService:
    def __init__(self):
        self.repository = UserRepository()

    def registrar_usuario(self, user_data: UserCreate):
        if user_data.rol not in ROLES_PERMITIDOS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El rol no es válido",
            )

        existing_user = self.repository.get_by_correo(user_data.correo)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ya existe un usuario registrado con ese correo",
            )

        hashed_pass = hash_password(user_data.password)
        return self.repository.create(user_data, hashed_pass)

    def eliminar_usuario(self, user_id: int) -> None:
        user = self.repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado",
            )
        self.repository.delete_by_id(user_id)
