from app.autenticacion.repository.auth_repository import auth_repository, MAX_INTENTOS
from app.autenticacion.domain.auth import LoginRequest, UsuarioAuthData
from app.core.security import verify_password, create_access_token

class CuentaBloqueadaError(Exception):
    pass

class IntentosFallidosError(Exception):
    def __init__(self, message: str, intentos_restantes: int):
        self.intentos_restantes = intentos_restantes
        super().__init__(message)

class AuthService:

    def __init__(self, repo):
        self.repo = repo

    def login(self, data: LoginRequest) -> dict:
        usuario = self.repo.get_by_correo(data.correo)

        if not usuario:
            raise ValueError("Correo no registrado en el sistema")
    
        if not usuario.activo:
            raise ValueError("La cuenta está inactiva. Contacte al administrador")

        if usuario.esta_bloqueado():
            raise CuentaBloqueadaError("Cuenta bloqueada temporalmente por múltiples intentos fallidos")

        if not verify_password(data.password, usuario.password):
            nuevos_intentos = usuario.intentos_fallidos + 1
            self.repo.actualizar_intentos(data.correo, nuevos_intentos)

            if nuevos_intentos >= MAX_INTENTOS:
                self.repo.bloquear_usuario(data.correo)
                raise CuentaBloqueadaError("Cuenta bloqueada temporalmente por múltiples intentos fallidos")

            restantes = MAX_INTENTOS - nuevos_intentos
            raise IntentosFallidosError("Contraseña incorrecta", restantes)

        self.repo.resetear_intentos(data.correo)

        token = create_access_token({
            "id": usuario.id,
            "correo": usuario.correo,
            "rol": usuario.rol,
            "nombre": usuario.nombre
        })

        usuario_data = UsuarioAuthData(
            id=usuario.id,
            nombre=usuario.nombre,
            correo=usuario.correo,
            rol=usuario.rol
        )

        return {
            "token": token,
            "tipo_token": "Bearer",
            "usuario": usuario_data.to_response()
        }

    def get_me(self, current_user: dict) -> dict:
        usuario_data = UsuarioAuthData(
            id=current_user.get("id"),
            nombre=current_user.get("nombre"),
            correo=current_user.get("correo"),
            rol=current_user.get("rol")
        )
        return usuario_data.to_response()

    def validar_token(self, current_user: dict) -> dict:
        usuario_data = UsuarioAuthData(
            id=current_user.get("id"),
            nombre=current_user.get("nombre"),
            correo=current_user.get("correo"),
            rol=current_user.get("rol")
        )
        return usuario_data.to_response()

    def logout(self, token: str) -> None:
        if self.repo.token_es_invalido(token):
            raise ValueError("El token proporcionado no es válido o ya fue revocado")
        self.repo.invalidar_token(token)

auth_service = AuthService(repo=auth_repository)