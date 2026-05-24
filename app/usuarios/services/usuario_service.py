from app.usuarios.repository.usuario_repo import UserRepository
from app.usuarios.domain.usuarios import ROLES_PERMITIDOS, UserCreate
from app.core.security import hash_password

class UserService:
    def __init__(self):
        self.repository = UserRepository()

    def registrar_usuario(self, user_data: UserCreate) -> dict:
        existing_user = self.repository.get_by_correo(user_data.correo)
        if existing_user:
            raise ValueError("Ya existe un usuario registrado con ese correo")
        hashed_pass = hash_password(user_data.password)
        user = self.repository.create(user_data, hashed_pass)
        return {
            "success": True,
            "statusCode": 201,
            "message": "Usuario registrado correctamente",
            "data": {
                "id": user.id,
                "nombre": user.nombre,
                "correo": user.correo,
                "rol": user.rol,
                "activo": user.activo
            }
        }
    
    def registrar_estudiante(self, user_data: UserCreate) -> dict:
        """Registro público — solo rol ESTUDIANTE."""
        if user_data.rol != "ESTUDIANTE":
            raise ValueError(
                "El endpoint de registro solo acepta rol ESTUDIANTE"
            )
        existing_user = self.repository.get_by_correo(user_data.correo)
        if existing_user:
            raise ValueError("Ya existe un usuario registrado con ese correo")
        hashed_pass = hash_password(user_data.password)
        user = self.repository.create(user_data, hashed_pass)
        return self._build_response(user)

    def eliminar_usuario(self, user_id: int) -> dict:
        user = self.repository.get_by_id(user_id)
        if not user:
            raise ValueError("Usuario no encontrado")
        self.repository.delete_by_id(user_id)
        return {
            "success": True,
            "statusCode": 200,
            "message": "Usuario eliminado correctamente"
        }
