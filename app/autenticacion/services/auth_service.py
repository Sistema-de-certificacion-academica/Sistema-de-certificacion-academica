# app/autenticacion/services/auth_service.py
# ─────────────────────────────────────────────────
# CAPA SERVICE — lógica de negocio de autenticación
# Coordina domain y repository
# Sin imports de FastAPI
# ─────────────────────────────────────────────────

from app.autenticacion.repository.auth_repository import auth_repository
from app.autenticacion.domain.auth import LoginRequest, LoginResponse
from app.core.security import verify_password, create_access_token


class AuthService:

    def __init__(self):
        self.repo = auth_repository

    def login(self, data: LoginRequest) -> dict:
        """
        Autentica el usuario y retorna token JWT.
        Aplica todas las reglas de negocio de HU-05.
        """

        # 1. Busca el usuario en el repository
        usuario = self.repo.get_by_correo(data.correo)

        # 2. Regla: el correo debe existir
        if not usuario:
            raise ValueError("Correo no registrado en el sistema")

        # 3. Regla del domain: el usuario no debe estar bloqueado
        if usuario.esta_bloqueado():
            raise ValueError("Cuenta bloqueada temporalmente")

        # 4. Regla: la contraseña debe ser correcta
        if not verify_password(data.password, usuario.password_hash):

            # Incrementa intentos fallidos
            nuevos_intentos = usuario.intentos_fallidos + 1
            self.repo.actualizar_intentos(data.correo, nuevos_intentos)

            # Regla del domain: bloquear si superó intentos
            if usuario.supero_intentos():
                self.repo.bloquear_usuario(data.correo)
                raise ValueError("Cuenta bloqueada por múltiples intentos fallidos")

            # Regla del domain: cuántos intentos le quedan
            raise ValueError(
                f"Contraseña incorrecta. "
                f"Intentos restantes: {usuario.intentos_restantes()}"
            )

        # 5. Login exitoso: resetea intentos
        self.repo.resetear_intentos(data.correo)

        # 6. Genera token JWT con datos del usuario
        token = create_access_token({
            "id": usuario.id,
            "correo": usuario.correo,
            "rol": usuario.rol,
            "nombre": usuario.nombre
        })

        # 7. Retorna respuesta según contrato de la HU
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
        """
        Retorna datos del usuario autenticado
        desde el payload del token JWT.
        """
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
        """
        Valida que el token JWT sea vigente.
        Si llega aquí el token ya fue validado
        por dependencies.py
        """
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


# Instancia única compartida
auth_service = AuthService()