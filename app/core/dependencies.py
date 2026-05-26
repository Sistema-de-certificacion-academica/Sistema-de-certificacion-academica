from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.security import decode_access_token
from datetime import datetime
from app.autenticacion.repository.auth_repository import auth_repository


security = HTTPBearer(auto_error=False)

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "success": False,
                "statusCode": 401,
                "message": "No autenticado",
                "error": {
                    "error_code": "UNAUTHORIZED",
                    "details": "Se requiere token de acceso para este recurso",
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                }
            }
        )

    token = credentials.credentials

    if auth_repository.token_es_invalido(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "success": False,
                "statusCode": 401,
                "message": "No autenticado",
                "error": {
                    "error_code": "UNAUTHORIZED",
                    "details": "El token fue revocado",
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                }
            }
        )

    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "success": False,
                "statusCode": 401,
                "message": "No autenticado",
                "error": {
                    "error_code": "UNAUTHORIZED",
                    "details": "Token inválido o expirado",
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                }
            }
        )
    return payload

def require_admin(current_user: dict = Depends(get_current_user)):
    if current_user.get("rol") != "ADMINISTRADOR":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "success": False,
                "statusCode": 403,
                "message": "Acceso denegado",
                "error": {
                    "error_code": "FORBIDDEN",
                    "details": "No tiene permisos para acceder a este recurso",
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                }
            }
        )
    return current_user

def require_estudiante(current_user: dict = Depends(get_current_user)):
    if current_user.get("rol") != "ESTUDIANTE":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "success": False,
                "statusCode": 403,
                "message": "Acceso denegado",
                "error": {
                    "error_code": "FORBIDDEN",
                    "details": "No tiene permisos para acceder a este recurso",
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                }
            }
        )
    return current_user

def require_empresa_externa(current_user: dict = Depends(get_current_user)):
    if current_user.get("rol") != "EMPRESA_EXTERNA":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "success": False,
                "statusCode": 403,
                "message": "Acceso denegado",
                "error": {
                    "error_code": "FORBIDDEN",
                    "details": "No tiene permisos para acceder a este recurso",
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                }
            }
        )
    return current_user

def require_estudiante_o_admin(current_user: dict = Depends(get_current_user)):
    rol = current_user.get("rol")
    if rol not in ["ESTUDIANTE", "ADMINISTRADOR"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "success": False,
                "statusCode": 403,
                "message": "Acceso denegado",
                "error": {
                    "error_code": "FORBIDDEN",
                    "details": "No tiene permisos para acceder a este recurso",
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                }
            }
        )
    return current_user