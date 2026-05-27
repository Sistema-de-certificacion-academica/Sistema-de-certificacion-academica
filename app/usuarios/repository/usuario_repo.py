
from typing import Optional
from app.usuarios.domain.usuarios import User
from app.usuarios.domain.usuarios import UserCreate
from app.core.security import hash_password


class UserRepository:
    _users: list[User] = []
    _next_id: int = 1
    _seeded: bool = False  

    def __init__(self):
        if not type(self)._seeded:
            self._seed()
            type(self)._seeded = True
    
    # Usuario administrador por defecto
    def _seed(self):
        admin = User(
            id=self._next_id,
            nombre="Admin UniCert",
            correo="admin@unicert.com",
            password=hash_password("admin123"),
            rol="ADMINISTRADOR",
            activo=True
        )
        type(self)._users.append(admin)
        type(self)._next_id += 1

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

    def update(self, user_id: int, nombre: str = None, correo: str = None, rol: str = None) -> User:
        user = self.get_by_id(user_id)
        if nombre is not None:
            user.nombre = nombre
        if correo is not None:
            user.correo = correo
        if rol is not None:
            user.rol = rol
        return user

    @classmethod
    def clear(cls):
        cls._users.clear()
        cls._next_id = 1

    def get_all(self, rol: str = None) -> list[User]:
        if rol:
            return [u for u in self._users if u.rol == rol]
        return self._users.copy()