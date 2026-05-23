from typing import Optional

from sqlalchemy.orm import Session
from app.usuarios.domain.models import User
from app.usuarios.domain.schemas import UserCreate


class UserRepository:

    def get_by_id(self, db: Session, user_id: int) -> Optional[User]:
        return db.query(User).filter(User.id == user_id).first()

    def get_by_correo(self, db: Session, correo: str) -> Optional[User]:
        return db.query(User).filter(User.correo == correo).first()

    def create(self, db: Session, user_data: UserCreate, hashed_password: str) -> User:
        db_user = User(
            nombre=user_data.nombre,
            correo=user_data.correo,
            password=hashed_password,
            rol=user_data.rol,
            activo=True,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
