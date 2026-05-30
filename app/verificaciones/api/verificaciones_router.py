from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Request, status
from app.core.dependencies import require_admin
from app.verificaciones.services.verificaciones_service import verificacion_service

router = APIRouter(prefix="/api/v1/verificaciones", tags=["Verificaciones"])

@router.post("/consultas", status_code=status.HTTP_201_CREATED)
def registrar_consulta(uuid_consultado: str, request: Request):
    ip = request.client.host
    return verificacion_service.registrar_consulta(uuid_consultado, ip)

@router.get("/consultas", status_code=status.HTTP_200_OK)
def listar_consultas(uuid: Optional[str] = None, current_user: dict = Depends(require_admin)):
    return verificacion_service.listar_consultas(uuid)

@router.get("/integridad/{uuid}", status_code=status.HTTP_200_OK)
def validar_integridad(uuid: str):
    try:
        return verificacion_service.validar_integridad(uuid)
    except ValueError as e:
        mensaje = str(e)
        if "formato" in mensaje.lower():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=mensaje)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=mensaje)

@router.get("/{codigo}", status_code=status.HTTP_200_OK)
def verificar_certificado(codigo: str, request: Request):
    ip = request.client.host
    try:
        return verificacion_service.verificar_certificado(codigo, ip)
    except ValueError as e:
        mensaje = str(e)
        if "formato" in mensaje.lower():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=mensaje)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=mensaje)
    