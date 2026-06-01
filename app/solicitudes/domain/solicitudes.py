from pydantic import BaseModel, Field, field_validator
from datetime import date
from app.plantillas.repository.plantillas_repo import plantilla_repository

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

class Solicitud:
    def __init__(self, id: int, usuario_id: int, tipo_certificado: str, comprobante_pago: str, estado: str = "PENDIENTE",
                 fecha_solicitud: str = None, motivo_rechazo: str = None):
        self.id = id
        self.usuario_id = usuario_id
        self.tipo_certificado = tipo_certificado
        self.comprobante_pago = comprobante_pago
        self.estado = estado
        self.fecha_solicitud = fecha_solicitud or date.today().isoformat()
        self.motivo_rechazo = motivo_rechazo

    def esta_pendiente(self) -> bool:
        return self.estado == "PENDIENTE"

    def puede_cancelarse(self) -> bool:
        return self.estado == "PENDIENTE"

    def to_response(self) -> dict:
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "tipo_certificado": self.tipo_certificado,
            "estado": self.estado,
            "comprobante_pago": self.comprobante_pago,
            "fecha_solicitud": self.fecha_solicitud
        }

    def to_response_gestion(self) -> dict:
        data = {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "tipo_certificado": self.tipo_certificado,
            "estado": self.estado,
            "fecha_solicitud": self.fecha_solicitud
        }
        if self.motivo_rechazo:
            data["motivo_rechazo"] = self.motivo_rechazo
        return data

class SolicitudCreate(BaseModel):
    tipo_certificado: str = Field(..., min_length=1)
    comprobante_pago: str = Field(..., min_length=1)

    @field_validator("tipo_certificado")
    @classmethod
    def validar_tipo(cls, v):
        plantilla = plantilla_repository.get_activa_by_tipo(v)
        if not plantilla:
            raise ValueError("No existe una plantilla activa para ese tipo de certificado")
        return v

    @field_validator("comprobante_pago")
    @classmethod
    def validar_comprobante(cls, v):
        if not v.strip():
            raise ValueError("El comprobante de pago no puede estar vacío")
        return v.strip()

class SolicitudResponse(BaseModel):
    id: int
    usuario_id: int
    tipo_certificado: str
    estado: str
    comprobante_pago: str
    fecha_solicitud: str

class ActualizarEstadoRequest(BaseModel):
    estado: str = Field(..., min_length=1)
    motivo_rechazo: str = None

    @field_validator("estado")
    @classmethod
    def validar_estado(cls, v):
        if v not in {"APROBADA", "RECHAZADA"}:
            raise ValueError("El estado solo puede ser APROBADA o RECHAZADA")
        return v