from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.usuarios.repository.usuario_repo import UserRepository
from app.usuarios.domain.schemas import UserCreate
from app.core.security import hash_password

class UserService:
    def __init__(self):
        self.repository = UserRepository()

    def registrar_usuario(self, db: Session, user_data: UserCreate):
        # 1. Validar que el correo no esté registrado previamente
        existing_user = self.repository.get_by_correo(db, user_data.correo)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ya existe un usuario registrado con ese correo",
            )

        # 2. Encriptar contraseña del usuario
        hashed_pass = hash_password(user_data.password)

        # 3. Guardar en base de datos
        return self.repository.create(db, user_data, hashed_pass)
