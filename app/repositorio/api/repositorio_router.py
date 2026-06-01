from fastapi import APIRouter, Depends, status, Response
from fastapi.responses import JSONResponse
from app.core.dependencies import require_estudiante_o_admin
from app.core.responses import success_response, error_response
from app.repositorio.services.repositorio_service import (repositorio_service, CertificadoAnuladoError, AccesoDenegadoError, UUIDInvalidoError)

router = APIRouter(prefix="/api/v1/repositorio", tags=["Repositorio"])

@router.get("/certificados/{uuid}", status_code=status.HTTP_200_OK)
def buscar_certificado(uuid: str, current_user: dict = Depends(require_estudiante_o_admin)):
    try:
        data = repositorio_service.buscar_certificado_por_uuid(
            uuid,
            current_user.get("id"),
            current_user.get("rol"),
        )
        return success_response(200, "Certificado encontrado", data)
    except AccesoDenegadoError as e:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content=error_response(403, "Acceso denegado", "FORBIDDEN", str(e)),
        )
    except ValueError as e:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=error_response(404, "No fue posible encontrar el certificado", "NOT_FOUND", str(e)),
        )

@router.get("/estudiantes/{id}", status_code=status.HTTP_200_OK)
def consultar_historial(id: int, current_user: dict = Depends(require_estudiante_o_admin)):
    try:
        data = repositorio_service.obtener_historial_estudiante(
            id,
            current_user.get("id"),
            current_user.get("rol"),
        )
        if not data:
            return success_response(200, "El estudiante no tiene certificados emitidos", [])
        return success_response(200, "Historial de certificados encontrado", data)
    except AccesoDenegadoError as e:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content=error_response(403, "Acceso denegado", "FORBIDDEN", str(e)))

@router.get("/metadatos/{uuid}", status_code=status.HTTP_200_OK)
def consultar_metadatos(uuid: str):
    try:
        data = repositorio_service.obtener_metadatos_publicos(uuid)
        return success_response(200, "Metadatos del certificado encontrados", data)
    except UUIDInvalidoError as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=error_response(400, "No fue posible consultar los metadatos", "BAD_REQUEST", str(e)))
    except ValueError as e:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=error_response(404, "No fue posible consultar los metadatos", "NOT_FOUND", str(e)))

@router.get("/descarga/{uuid}", status_code=status.HTTP_200_OK)
def descargar_certificado(uuid: str, current_user: dict = Depends(require_estudiante_o_admin)):
    try:
        pdf_bytes = repositorio_service.descargar_pdf_certificado(
            uuid,
            current_user.get("id"),
            current_user.get("rol"),
        )
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f'attachment; filename="certificado_{uuid}.pdf"'
            },
        )
    except CertificadoAnuladoError as e:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=error_response(409, "No fue posible descargar el certificado", "CONFLICT", str(e)),
        )
    except AccesoDenegadoError as e:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content=error_response(403, "Acceso denegado", "FORBIDDEN", str(e)),
        )
    except ValueError as e:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=error_response(404, "No fue posible descargar el certificado", "NOT_FOUND", str(e)),
        )