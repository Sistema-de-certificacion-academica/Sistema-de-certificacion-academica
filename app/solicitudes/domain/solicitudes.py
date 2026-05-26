from pydantic import BaseModel, Field, field_validator
from datetime import date

TIPOS_CERTIFICADO = frozenset({
    "CERTIFICADO_ESTUDIO",
    "CERTIFICADO_NOTAS",
    "CERTIFICADO_GRADUACION",
    "CERTIFICADO_CONDUCTA",
    "PAZ_Y_SALVO"
})

ESTADOS_SOLICITUD = frozenset({
    "PENDIENTE",
    "APROBADA",
    "RECHAZADA"
})

class SolicitudCreate(BaseModel):
    tipo_certificado: str = Field(..., min_length=1)
    comprobante_pago: str = Field(..., min_length=1)

    @field_validator("tipo_certificado")
    @classmethod
    def validar_tipo(cls, v):
        if v not in TIPOS_CERTIFICADO:
            raise ValueError(
                f"Tipo de certificado no válido. "
                f"Tipos permitidos: {', '.join(TIPOS_CERTIFICADO)}"
            )
        return v

    @field_validator("comprobante_pago")
    @classmethod
    def validar_comprobante(cls, v):
        if not v.strip():
            raise ValueError("El comprobante de pago no puede estar vacío")
        return v.strip()

class Solicitud:
    def __init__(self, id: int, usuario_id: int, tipo_certificado: str, comprobante_pago: str, 
                 estado: str = "PENDIENTE", fecha_solicitud: str = None):
        self.id = id
        self.usuario_id = usuario_id
        self.tipo_certificado = tipo_certificado
        self.comprobante_pago = comprobante_pago
        self.estado = estado
        self.fecha_solicitud = fecha_solicitud or date.today().isoformat()

    def esta_pendiente(self) -> bool:
        return self.estado == "PENDIENTE"

    def puede_cancelarse(self) -> bool:
        return self.estado == "PENDIENTE"

class SolicitudResponse(BaseModel):
    id: int
    usuario_id: int
    tipo_certificado: str
    estado: str
    comprobante_pago: str
    fecha_solicitud: str