from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.security import decode_access_token

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    from app.autenticacion.repository.auth_repository import auth_repository
    
    token = credentials.credentials  

    if auth_repository.token_es_invalido(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o ya fue revocado",
            headers={"WWW-Authenticate": "Bearer"}
        )

    payload = decode_access_token(token) 

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return payload

def require_admin(current_user: dict = Depends(get_current_user)):
    if current_user.get("rol") != "ADMINISTRADOR":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permisos para acceder a este recurso"
        )
    return current_user

def require_estudiante(current_user: dict = Depends(get_current_user)):
    if current_user.get("rol") != "ESTUDIANTE":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permisos para acceder a este recurso"
        )
    return current_user