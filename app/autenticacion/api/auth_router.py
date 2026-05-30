from fastapi import APIRouter, Depends, HTTPException, status
from app.autenticacion.domain.auth import LoginRequest
from app.autenticacion.services.auth_service import auth_service
from app.core.dependencies import get_current_user
from fastapi.security import HTTPAuthorizationCredentials
from app.core.dependencies import security
from datetime import datetime

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Autenticación"]
)

@router.post("/login", status_code=status.HTTP_200_OK)
def login(data: LoginRequest):
    try:
        return auth_service.login(data)
    except ValueError as e:
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
                    "error_message": "Contraseña incorrecta",
                    "intentos_restantes": int(mensaje.split("Intentos restantes: ")[1]),
                    "sugerencia": "Verifique que la tecla Mayúsculas no esté activada."
                }
            }
        )

@router.get("/me", status_code=status.HTTP_200_OK)
def get_me(current_user: dict = Depends(get_current_user)):
    try:
        return auth_service.get_me(current_user)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

@router.get("/validar", status_code=status.HTTP_200_OK)
def validar_token(current_user: dict = Depends(get_current_user)):
    try:
        return auth_service.validar_token(current_user)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    
@router.post("/logout", status_code=status.HTTP_200_OK)
def logout(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        return auth_service.logout(token)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )