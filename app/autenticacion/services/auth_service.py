from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from core.security import verify_password, create_access_token
from autenticacion.repository.auth_repo import AuthRepository

INTENTOS_MAX = 5

class AuthService:

    def __init__(self):
        self.repo = AuthRepository()

    # Autentica el usuario y retorna token
    def login(self, correo: str, password: str, db: Session) -> dict:

        usuario = self.repo.get_usuario_por_correo(correo, db)

        # El correo debe existir
        if not usuario:
            raise HTTPException(
               us_code=status.HTTP_401_UNAUTHORIZED,
                 statdetail={
                    "success": False,
                    "statusCode": 401,
                    "message": "No se pudo iniciar sesión",
                    "error": {
                        "error_code": 401,
                        "error_message": "Correo no registrado en el sistema",
                        "intentos_restantes": None,
                        "sugerencia": "Verifique que el correo sea correcto"
                    }
                }
            )

        # El usuario no debe estar bloqueado
        if usuario.bloqueado:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "success": False,
                    "statusCode": 403,
                    "message": "Cuenta bloqueada temporalmente",
                    "error": {
                        "error_code": 403,
                        "error_message": "Su cuenta fue bloqueada por múltiples intentos fallidos",
                        "sugerencia": "Contacte al administrador para desbloquear su cuenta"
                    }
                }
            )

        # La contraseña debe ser correcta
        if not verify_password(password, usuario.password):
            nuevos_intentos = usuario.intentos_fallidos + 1

            # Bloquea después de 5 intentos
            if nuevos_intentos >= INTENTOS_MAX:
                self.repo.bloquear_usuario(correo, db)
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail={
                        "success": False,
                        "statusCode": 403,
                        "message": "Cuenta bloqueada temporalmente",
                        "error": {
                            "error_code": 403,
                            "error_message": "Ha superado el límite de intentos fallidos",
                            "sugerencia": "Contacte al administrador para desbloquear su cuenta"
                        }
                    }
                )

            self.repo.actualizar_intentos_fallidos(correo, nuevos_intentos, db)

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "success": False,
                    "statusCode": 401,
                    "message": "No se pudo iniciar sesión",
                    "error": {
                        "error_code": 401,
                        "error_message": "Contraseña incorrecta",
                        "intentos_restantes": INTENTOS_MAX - nuevos_intentos,
                        "sugerencia": "Verifique que la tecla Mayúsculas no esté activada."
                    }
                }
            )

        self.repo.resetear_intentos(correo, db)

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

    # Retorna usuario autenticado 
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