from typing import Optional

from app.usuarios.domain.models import User
from app.usuarios.domain.schemas import UserCreate


class UserRepository:
    _users: list[User] = []
    _next_id: int = 1

    def get_by_id(self, user_id: int) -> Optional[User]:
        for user in self._users:
            if user.id == user_id:
                return user
        return None

    def delete_by_id(self, user_id: int) -> bool:
        for i, user in enumerate(self._users):
            if user.id == user_id:
                self._users.pop(i)
                return True
        return False

    def get_by_correo(self, correo: str) -> Optional[User]:
        for user in self._users:
            if user.correo == correo:
                return user
        return None

    def create(self, user_data: UserCreate, hashed_password: str) -> User:
        user = User(
            id=self._next_id,
            nombre=user_data.nombre,
            correo=user_data.correo,
            password=hashed_password,
            rol=user_data.rol,
            activo=True,
        )
        self._users.append(user)
        type(self)._next_id += 1
        return user

    @classmethod
    def clear(cls):
        cls._users.clear()
        cls._next_id = 1
