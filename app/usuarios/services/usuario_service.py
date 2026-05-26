from app.usuarios.repository.usuario_repo import UserRepository
from app.usuarios.domain.usuarios import ROLES_PERMITIDOS, UserCreate
from app.core.security import hash_password
from app.solicitudes.repository.solicitudes_repo import solicitud_repository

class ConflictError(Exception):
    pass

class UserService:
    def __init__(self):
        self.repository = UserRepository()

    def _build_response(self, user) -> dict:
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

    def registrar_usuario(self, user_data: UserCreate) -> dict:
        existing_user = self.repository.get_by_correo(user_data.correo)
        if existing_user:
            raise ValueError("Ya existe un usuario registrado con ese correo")
        hashed_pass = hash_password(user_data.password)
        user = self.repository.create(user_data, hashed_pass)
        return self._build_response(user)
    
    def registrar_estudiante(self, user_data: UserCreate) -> dict:
        if user_data.rol != "ESTUDIANTE":
            raise ValueError("El endpoint de registro solo acepta rol ESTUDIANTE")
        existing_user = self.repository.get_by_correo(user_data.correo)
        if existing_user:
            raise ValueError("Ya existe un usuario registrado con ese correo")
        hashed_pass = hash_password(user_data.password)
        user = self.repository.create(user_data, hashed_pass)
        return self._build_response(user)
    
    def eliminar_usuario(self, user_id: int, admin_id: int) -> dict:
        # Regla: el usuario debe existir
        usuario = self.repository.get_by_id(user_id)
        if not usuario:
            raise ValueError("No existe un usuario con el id proporcionado")

        # Regla: no puede eliminarse a sí mismo
        if user_id == admin_id:
            raise ValueError("No puede eliminarse a si mismo")

        # Regla: no puede tener solicitudes pendientes
        solicitudes = solicitud_repository.get_by_usuario(user_id)
        pendientes = [s for s in solicitudes if s.estado == "PENDIENTE"]
        if pendientes:
            raise ConflictError("El usuario tiene solicitudes de certificado pendientes")

        self.repository.delete_by_id(user_id)

        return {
            "success": True,
            "statusCode": 204,
            "message": "Usuario eliminado correctamente",
            "data": None
        }

usuario_services = UserService()
