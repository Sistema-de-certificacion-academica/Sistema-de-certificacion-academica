from pydantic import BaseModel, Field
from typing import Optional


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
    ruta_pdf: Optional[str] = None

    class Config:
        from_attributes = True


class CertificateAnuladoResponse(BaseModel):
    id: int
    uuid: str
    estado: str
    fecha_emision: str
    estudiante: dict = Field(default_factory=dict)


class CertificatePatchEstado(BaseModel):
    estado: str = Field(..., pattern=r"^ANULADO$")


class Certificate:
    def __init__(self, id: int, uuid: str, solicitud_id: int, plantilla_id: int,
                 estado: str = "GENERADO", fecha_emision: str = None, ruta_pdf: str = None):
        self.id = id
        self.uuid = uuid
        self.solicitud_id = solicitud_id
        self.plantilla_id = plantilla_id
        self.estado = estado
        self.fecha_emision = fecha_emision
        self.ruta_pdf = ruta_pdf

    def esta_anulado(self) -> bool:
        return self.estado == "ANULADO"

    def to_response(self) -> dict:
        return {
            "id": self.id,
            "uuid": self.uuid,
            "solicitud_id": self.solicitud_id,
            "plantilla_id": self.plantilla_id,
            "estado": self.estado,
            "fecha_emision": self.fecha_emision,
            "ruta_pdf": self.ruta_pdf,
        }

    def to_anulado_response(self) -> dict:
        estudiante = {}
        if self.nombre_estudiante:
            estudiante = {
                "nombre": self.nombre_estudiante,
                "programa_academico": self.programa_academico,
            }

        return {
            "id": self.id,
            "uuid": self.uuid,
            "estado": self.estado,
            "fecha_emision": self.fecha_emision,
            "estudiante": estudiante,
        }
