from pydantic import BaseModel, Field

class Certificate:
    def __init__(self, id: int, uuid: str, solicitud_id: int, plantilla_id: int,
                 estado: str = "GENERADO", fecha_emision: str = None, ruta_pdf: str = None,
                 nombre_estudiante: str = None, programa_academico: str = None):
        self.id = id
        self.uuid = uuid
        self.solicitud_id = solicitud_id
        self.plantilla_id = plantilla_id
        self.estado = estado
        self.fecha_emision = fecha_emision
        self.ruta_pdf = ruta_pdf
        self.nombre_estudiante = nombre_estudiante
        self.programa_academico = programa_academico

class CertificateCreate(BaseModel):
    solicitud_id: int = Field(..., gt=0)
    plantilla_id: int = Field(..., gt=0)

class CertificateResponse(BaseModel):
    id: int
    uuid: str
    solicitud_id: int
    plantilla_id: int
    estado: str
    fecha_emision: str
    ruta_pdf: str = None

    class Config:
        from_attributes = True

class CertificatePatchEstado(BaseModel):
    estado: str = Field(..., pattern=r"^ANULADO$")
