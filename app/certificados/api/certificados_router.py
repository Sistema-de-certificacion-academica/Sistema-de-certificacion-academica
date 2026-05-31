from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from app.core.dependencies import require_admin
from app.core.responses import error_response, success_response
from app.certificados.domain.certificados import CertificateCreate, CertificatePatchEstado
from app.certificados.services.certificados_service import certificate_service

router = APIRouter(prefix="/api/v1/certificados", tags=["Certificados"])
@router.post("", status_code=status.HTTP_201_CREATED)
def generar_certificado(data: CertificateCreate, current_user: dict = Depends(require_admin)):
    try:
        certificado = certificate_service.generar_certificado(data)
        return success_response(
            status_code=status.HTTP_201_CREATED,
            message="Certificado generado correctamente",
            data=certificado.model_dump(),
        )
    except ValueError as e:
        mensaje = str(e)
        if "no esta aprobada" in mensaje or "no esta activa" in mensaje:
            status_code = status.HTTP_409_CONFLICT
            error_code = "CERTIFICATE_CONFLICT"
        else:
            status_code = status.HTTP_404_NOT_FOUND
            error_code = "CERTIFICATE_NOT_FOUND"
        return JSONResponse(
            status_code=status_code,
            content=error_response(
                status_code=status_code,
                message="No se pudo generar el certificado",
                error_code=error_code,
                details=mensaje,
            ),
        )
@router.patch("/{id}/estado", status_code=status.HTTP_200_OK)
def anular_certificado(id: int, data: CertificatePatchEstado, current_user: dict = Depends(require_admin)):
    try:
        certificado = certificate_service.anular_certificado(id, data.estado)
        return success_response(
            status_code=status.HTTP_200_OK,
            message="Certificado anulado correctamente",
            data=certificado.model_dump(),
        )
    except ValueError as e:
        mensaje = str(e)
        if "ya esta anulado" in mensaje:
            status_code = status.HTTP_409_CONFLICT
            error_code = "CERTIFICATE_ALREADY_CANCELLED"
        else:
            status_code = status.HTTP_404_NOT_FOUND
            error_code = "CERTIFICATE_NOT_FOUND"
        return JSONResponse(
            status_code=status_code,
            content=error_response(
                status_code=status_code,
                message="No se pudo anular el certificado",
                error_code=error_code,
                details=mensaje,
            ),
        )