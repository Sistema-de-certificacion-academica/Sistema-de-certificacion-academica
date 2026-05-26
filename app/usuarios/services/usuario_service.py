from app.usuarios.repository.usuario_repo import UserRepository
from app.usuarios.domain.usuarios import ROLES_ACTUALIZABLES, ROLES_PERMITIDOS, UserCreate, UserUpdate
from app.core.security import hash_password
from app.solicitudes.repository.solicitudes_repo import solicitud_repository

class ConflictError(Exception):
    pass

class ServiceError(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(message)

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

    def _build_update_response(self, user) -> dict:
        return {
            "success": True,
            "statusCode": 200,
            "message": "Usuario actualizado correctamente",
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

    def obtener_usuario_por_id(self, usuario_id: int) -> dict:
        user = self.repository.get_by_id(usuario_id)
        if user is None:
            raise ServiceError(
                "No existe un usuario con el id proporcionado", 404
            )
        return {
            "success": True,
            "statusCode": 200,
            "message": "Usuario encontrado",
            "data": {
                "id": user.id,
                "nombre": user.nombre,
                "correo": user.correo,
                "rol": user.rol,
                "activo": user.activo
            }
        }

    def actualizar_perfil_usuario(self, usuario_id: int, user_data: UserUpdate) -> dict:
        user = self.repository.get_by_id(usuario_id)
        if user is None:
            raise ServiceError(
                "No existe un usuario con el id proporcionado", 404
            )

        if user_data.correo is not None and user_data.correo != user.correo:
            existing = self.repository.get_by_correo(user_data.correo)
            if existing is not None and existing.id != usuario_id:
                raise ServiceError(
                    "El correo electrónico ya está en uso por otro usuario", 409
                )

        if user_data.rol is not None and user_data.rol not in ROLES_ACTUALIZABLES:
            raise ServiceError(
                "El rol no es válido. Los roles permitidos son: ESTUDIANTE, ADMINISTRADOR", 400
            )

        updated_user = self.repository.update(
            usuario_id,
            nombre=user_data.nombre,
            correo=user_data.correo,
            rol=user_data.rol
        )
        return self._build_update_response(updated_user)

usuario_services = UserService()

