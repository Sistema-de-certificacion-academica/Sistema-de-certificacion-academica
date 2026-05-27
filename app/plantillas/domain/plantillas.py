class Plantilla:
    def __init__(self, id: int, nombre: str, tipo_certificado: str, estructura: list, activa: bool = True):
        self.id = id
        self.nombre = nombre
        self.tipo_certificado = tipo_certificado
        self.estructura = estructura
        self.activa = activa

from pydantic import BaseModel, Field, field_validator

class TemplateCreate(BaseModel):
    nombre: str = Field(..., min_length=1)
    tipo_certificado: str = Field(..., min_length=1)
    estructura: list

    @field_validator("estructura")
    @classmethod
    def validar_estructura(cls, v):
        if not isinstance(v, list) or len(v) == 0:
            raise ValueError("La estructura debe contener al menos un campo")
        return v

class TemplateResponse(BaseModel):
    id: int
    nombre: str
    tipo_certificado: str
    estructura: list
    activa: bool

    class Config:
        from_attributes = True
