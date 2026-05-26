from app.solicitudes.repository.solicitudes_repo import solicitud_repository
from app.solicitudes.domain.solicitudes import SolicitudCreate

class SolicitudService:

    def __init__(self):
        self.repo = solicitud_repository

    def crear_solicitud(self,usuario_id: int, data: SolicitudCreate) -> dict:
        solicitud_existente = self.repo.get_by_usuario_y_tipo(usuario_id,data.tipo_certificado)
        if solicitud_existente: 
            raise ValueError("Ya tienes una solicitud pendiente de ese tipo de certificado")

        solicitud = self.repo.create(usuario_id, data)

        return self._build_response(solicitud)

    def _build_response(self, solicitud) -> dict:
        return {
            "success": True,
            "statusCode": 201,
            "message": "Solicitud creada correctamente",
            "data": {
                "id": solicitud.id,
                "usuario_id": solicitud.usuario_id,
                "tipo_certificado": solicitud.tipo_certificado,
                "estado": solicitud.estado,
                "comprobante_pago": solicitud.comprobante_pago,
                "fecha_solicitud": solicitud.fecha_solicitud
            }
        }

solicitud_service = SolicitudService()