from fastapi import APIRouter, Depends, HTTPException, status
from app.core.dependencies import require_admin
from app.certificados.domain.certificados import CertificateCreate
from app.certificados.services.certificados_service import certificate_service

router = APIRouter(prefix="/api/v1/certificados", tags=["Certificados"])

@router.post("", status_code=status.HTTP_201_CREATED)
def generar_certificado(data: CertificateCreate, current_user: dict = Depends(require_admin)):
    try:
        return certificate_service.generar_certificado(data)
    except ValueError as e:
        mensaje = str(e)
        if "no está aprobada" in mensaje or "no está activa" in mensaje:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=mensaje
            )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=mensaje
        )
