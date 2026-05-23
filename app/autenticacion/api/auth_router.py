# app/autenticacion/api/auth_router.py
# ─────────────────────────────────────────────────
# CAPA API — endpoints HTTP de autenticación
# Solo recibe peticiones y llama al service
# Convierte ValueError en HTTPException
# Sin lógica de negocio aquí
# ─────────────────────────────────────────────────

from fastapi import APIRouter, Depends, HTTPException, status
from app.autenticacion.domain.auth import LoginRequest
from app.autenticacion.services.auth_service import auth_service
from app.core.dependencies import get_current_user

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Autenticación"]
)


# ── POST /api/v1/auth/login ───────────────────────
@router.post("/login", status_code=status.HTTP_200_OK)
def login(data: LoginRequest):
    """
    HU-05: Autentica usuario y genera token JWT.
    No requiere autenticación previa.
    """
    try:
        return auth_service.login(data)
    except ValueError as e:
        # Determina el código HTTP según el error
        mensaje = str(e)
        if "bloqueada" in mensaje.lower():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "success": False,
                    "statusCode": 403,
                    "message": mensaje,
                    "error": {
                        "error_code": 403,
                        "error_message": mensaje,
                        "sugerencia": "Contacte al administrador"
                    }
                }
            )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "success": False,
                "statusCode": 401,
                "message": "No se pudo iniciar sesión",
                "error": {
                    "error_code": 401,
                    "error_message": mensaje,
                    "sugerencia": "Verifique que la tecla Mayúsculas no esté activada."
                }
            }
        )


# ── GET /api/v1/auth/me ───────────────────────────
@router.get("/me", status_code=status.HTTP_200_OK)
def get_me(
    current_user: dict = Depends(get_current_user)
):
    """
    HU-05: Retorna datos del usuario autenticado.
    Requiere token válido en el header.
    """
    try:
        return auth_service.get_me(current_user)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )


# ── GET /api/v1/auth/validar ──────────────────────
@router.get("/validar", status_code=status.HTTP_200_OK)
def validar_token(
    current_user: dict = Depends(get_current_user)
):
    """
    HU-05: Valida que el token JWT sea vigente.
    Requiere token válido en el header.
    """
    try:
        return auth_service.validar_token(current_user)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )