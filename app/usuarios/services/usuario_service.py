from app.usuarios.repository.usuario_repo import UserRepository
from app.usuarios.domain.usuarios import ROLES_ACTUALIZABLES, ROLES_PERMITIDOS, UserCreate, UserUpdate
from app.core.security import hash_password
from app.solicitudes.repository.solicitudes_repo import solicitud_repository

class ConflictError(Exception):
    pass

class RolInvalidoError(ValueError):     
    pass

class AutoeliminacionError(ValueError):
    pass

class UserService:
    def __init__(self, repo: UserRepository):
        self.repository = repo

    def registrar_usuario(self, user_data: UserCreate) -> dict:
        if self.repository.get_by_correo(user_data.correo):
            raise ConflictError("Ya existe un usuario registrado con ese correo")
        hashed_pass = hash_password(user_data.password)
        user = self.repository.create(user_data, hashed_pass)
        return user.to_response()

    def registrar_estudiante(self, user_data: UserCreate) -> dict:
        if user_data.rol != "ESTUDIANTE":
            raise RolInvalidoError("El endpoint de registro solo acepta rol ESTUDIANTE")
        if self.repository.get_by_correo(user_data.correo):
            raise ConflictError("Ya existe un usuario registrado con ese correo")
        hashed_pass = hash_password(user_data.password)
        user = self.repository.create(user_data, hashed_pass)
        return user.to_response()

    def obtener_usuario_por_id(self, usuario_id: int) -> dict:
        user = self.repository.get_by_id(usuario_id)
        if user is None:
            raise ValueError("No existe un usuario con el id proporcionado")
        return user.to_response()

    def listar_usuarios(self, rol: str = None) -> list:
        if rol and rol not in ROLES_PERMITIDOS:
            raise ValueError("El rol proporcionado no es válido")
        usuarios = self.repository.get_all(rol)
        return [u.to_response() for u in usuarios]

    def actualizar_perfil_usuario(self, usuario_id: int, user_data: UserUpdate) -> dict:
        user = self.repository.get_by_id(usuario_id)
        if user is None:
            raise ValueError("No existe un usuario con el id proporcionado")
        if user_data.correo is not None and user_data.correo != user.correo:
            existing = self.repository.get_by_correo(user_data.correo)
            if existing is not None and existing.id != usuario_id:
                raise ConflictError("El correo ya está en uso")
        if user_data.rol is not None and user_data.rol not in ROLES_ACTUALIZABLES:
            raise RolInvalidoError("El rol no es válido")
        updated = self.repository.update(
            usuario_id,
            nombre=user_data.nombre,
            correo=user_data.correo,
            rol=user_data.rol
        )
        return updated.to_response()

    def eliminar_usuario(self, user_id: int, admin_id: int) -> None:
        usuario = self.repository.get_by_id(user_id)
        if not usuario:
            raise ValueError("No existe un usuario con el id proporcionado")
        if user_id == admin_id:
            raise AutoeliminacionError("No puede eliminarse a si mismo")
        solicitudes = solicitud_repository.get_by_usuario(user_id)
        if any(s.estado == "PENDIENTE" for s in solicitudes):
            raise ConflictError("El usuario tiene solicitudes de certificado pendientes")
        self.repository.delete_by_id(user_id)

usuario_services = UserService(repo=UserRepository())