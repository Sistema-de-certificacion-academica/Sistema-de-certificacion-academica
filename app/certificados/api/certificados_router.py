from fastapi import APIRouter, Depends, HTTPException, status
from app.core.dependencies import require_admin
from app.certificados.domain.certificados import CertificateCreate, CertificatePatchEstado
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

@router.patch("/{id}/estado", status_code=status.HTTP_200_OK)
def anular_certificado(id: int, data: CertificatePatchEstado, current_user: dict = Depends(require_admin)):
    try:
        return certificate_service.anular_certificado(id)
    except ValueError as e:
        mensaje = str(e)
        if "ya está anulado" in mensaje:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=mensaje
            )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=mensaje
        )
