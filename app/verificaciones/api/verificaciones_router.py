from typing import Optional
from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import JSONResponse
from app.core.dependencies import require_admin
from app.core.responses import success_response, error_response
from app.verificaciones.services.verificaciones_service import (verificacion_service, UUIDInvalidoError)

router = APIRouter(prefix="/api/v1/verificaciones", tags=["Verificaciones"])

@router.get("/consultas", status_code=status.HTTP_200_OK)
def listar_consultas(uuid: Optional[str] = None, current_user: dict = Depends(require_admin)):
    data = verificacion_service.listar_consultas(uuid)
    if not data:
        return success_response(200, "No hay consultas registradas", [])
    return success_response(200, "Historial de verificaciones encontrado", data)

@router.get("/integridad/{uuid}", status_code=status.HTTP_200_OK)
def validar_integridad(uuid: str):
    try:
        data = verificacion_service.validar_integridad(uuid)
        return success_response(200, "Integridad del certificado verificada", data)
    except UUIDInvalidoError as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=error_response(400, "No fue posible verificar la integridad","BAD_REQUEST", str(e)),
        )
    except ValueError as e:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=error_response(404, "No fue posible verificar la integridad","NOT_FOUND", str(e))
            )

@router.get("/{codigo}", status_code=status.HTTP_200_OK)
def verificar_certificado(codigo: str, request: Request):
    ip = request.client.host
    try:
        data = verificacion_service.verificar_certificado(codigo, ip)
        mensaje = ("Certificado verificado correctamente" if data.get("valido") else "Certificado no válido")
        return success_response(200, mensaje, data)
    except UUIDInvalidoError as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=error_response(400, "No fue posible verificar el certificado","BAD_REQUEST", str(e)),
        )
    except ValueError as e:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=error_response(404, "Certificado no encontrado", "NOT_FOUND", str(e)),
        )

