from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from core.dependencies import get_db, get_current_user
from autenticacion.domain.models import LoginRequest
from autenticacion.services.auth_service import AuthService

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Autenticación"]
)

service = AuthService()

tokens_invalidados = set()

@router.post("/login", status_code=status.HTTP_200_OK)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    return service.login(data.correo, data.password, db)

@router.post("/logout", status_code=status.HTTP_200_OK)
def logout(current_user: dict = Depends(get_current_user), token: str = Depends(get_current_user)):
    tokens_invalidados.add(token)

    return {
        "success": True,
        "statusCode": 200,
        "message": "Sesión cerrada correctamente",
        "data": None
    }

@router.get("/me", status_code=status.HTTP_200_OK)
def get_me(current_user: dict = Depends(get_current_user)):
    return service.get_me(current_user)

@router.get("/validar", status_code=status.HTTP_200_OK)
def validar_token(current_user: dict = Depends(get_current_user)):
    return service.validar_token(current_user)