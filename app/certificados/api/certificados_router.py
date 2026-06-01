from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from app.core.dependencies import require_admin
from app.core.responses import success_response, error_response
from app.certificados.domain.certificados import CertificateCreate
from app.certificados.services.certificados_service import (
    certificate_service, SolicitudNoAprobadaError,
    PlantillaInactivaError, CertificadoYaAnuladoError
)

router = APIRouter(prefix="/api/v1/certificados", tags=["Certificados"])


@router.post("", status_code=status.HTTP_201_CREATED)
def generar_certificado(data: CertificateCreate, current_user: dict = Depends(require_admin)):
    try:
        data_response = certificate_service.generar_certificado(data)
        return success_response(201, "Certificado generado correctamente", data_response)
    except SolicitudNoAprobadaError as e:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=error_response(409, "No fue posible generar el certificado", "CONFLICT", str(e))
        )
    except PlantillaInactivaError as e:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=error_response(409, "No fue posible generar el certificado", "CONFLICT", str(e))
        )
    except ValueError as e:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=error_response(404, "No fue posible generar el certificado", "NOT_FOUND", str(e))
        )


@router.patch("/{id}/anular", status_code=status.HTTP_200_OK)
def anular_certificado(id: int , current_user: dict = Depends(require_admin)):
    try:
        data_response = certificate_service.anular_certificado(id)
        return success_response(200, "Certificado anulado correctamente", data_response)
    except CertificadoYaAnuladoError as e:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=error_response(409, "No fue posible anular el certificado", "CONFLICT", str(e))
        )
    except ValueError as e:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=error_response(404, "No fue posible anular el certificado", "NOT_FOUND", str(e))
        )