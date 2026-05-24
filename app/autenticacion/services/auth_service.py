from app.autenticacion.repository.auth_repository import auth_repository
from app.autenticacion.domain.auth import LoginRequest 
from app.core.security import verify_password, create_access_token


class AuthService:

    def __init__(self):
        self.repo = auth_repository

    def login(self, data: LoginRequest) -> dict:
        usuario = self.repo.get_by_correo(data.correo)

        if not usuario:
            raise ValueError("Correo no registrado en el sistema")

        if usuario.bloqueado:
            raise ValueError("Cuenta bloqueada temporalmente")

        if not verify_password(data.password, usuario.password):

            nuevos_intentos = usuario.intentos_fallidos + 1
            self.repo.actualizar_intentos(data.correo, nuevos_intentos)

            if nuevos_intentos >= 5:
                self.repo.bloquear_usuario(data.correo)
                raise ValueError("Cuenta bloqueada por múltiples intentos fallidos")

            raise ValueError(
                f"Contraseña incorrecta. "
                f"Intentos restantes: {5 - nuevos_intentos}"
            )

        self.repo.resetear_intentos(data.correo)

        token = create_access_token({
            "id": usuario.id,
            "correo": usuario.correo,
            "rol": usuario.rol,
            "nombre": usuario.nombre
        })

        return {
            "success": True,
            "statusCode": 200,
            "message": "Inicio de sesión exitoso",
            "data": {
                "token": token,
                "tipo_token": "Bearer",
                "usuario": {
                    "id": usuario.id,
                    "nombre": usuario.nombre,
                    "correo": usuario.correo,
                    "rol": usuario.rol
                }
            }
        }

    def get_me(self, current_user: dict) -> dict:
        return {
            "success": True,
            "statusCode": 200,
            "message": "Usuario autenticado",
            "data": {
                "id": current_user.get("id"),
                "nombre": current_user.get("nombre"),
                "correo": current_user.get("correo"),
                "rol": current_user.get("rol")
            }
        }

    def validar_token(self, current_user: dict) -> dict:
        return {
            "success": True,
            "statusCode": 200,
            "message": "Token válido",
            "data": {
                "id": current_user.get("id"),
                "nombre": current_user.get("nombre"),
                "correo": current_user.get("correo"),
                "rol": current_user.get("rol")
            }
        }

auth_service = AuthService()