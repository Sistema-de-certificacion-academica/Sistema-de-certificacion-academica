from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.core.security import decode_access_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


# Abre y cierra sesion por cada  peticion
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Lee token y retorna usuairo autenticado
def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    payload = decode_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",#AQUI CAMBIÉ EL MESSAGE POR DETAIL YA QUE GENERABA ERROR
            headers={"WWW-Authenticate": "Bearer"},
        )

    return payload


# Verifica rol admin
def require_admin(current_user: dict = Depends(get_current_user)):
    if current_user.get("rol") != "ADMINISTRADOR":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permisos para acceder a este recurso",
        )
    return current_user


# Verifica rol estudiante
def require_estudiante(current_user: dict = Depends(get_current_user)):
    if current_user.get("rol") != "ESTUDIANTE":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permisos para acceder a este recurso",
        )
    return current_user

