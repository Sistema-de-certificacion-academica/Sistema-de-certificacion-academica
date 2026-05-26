from app.solicitudes.repository.solicitudes_repo import solicitud_repository
from app.solicitudes.domain.solicitudes import SolicitudCreate, ActualizarEstadoRequest

class ConflictError(Exception):
    pass

class SolicitudService:

    def __init__(self):
        self.repo = solicitud_repository

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

    def crear_solicitud(self,usuario_id: int, data: SolicitudCreate) -> dict:
        solicitud_existente = self.repo.get_by_usuario_y_tipo(usuario_id,data.tipo_certificado)
        if solicitud_existente: 
            raise ValueError("Ya tienes una solicitud pendiente de ese tipo de certificado")

        solicitud = self.repo.create(usuario_id, data)

        return self._build_response(solicitud)
    
    def consultar_solicitud(self, solicitud_id: int, usuario_id: int, rol: str) -> dict:
        solicitud = self.repo.get_by_id(solicitud_id)

        if not solicitud:
            raise ValueError("No existe una solicitud con el id proporcionado")

        if rol == "ESTUDIANTE" and solicitud.usuario_id != usuario_id:
            raise PermissionError("No tiene permisos para consultar esta solicitud")

        return {
            "success": True,
            "statusCode": 200,
            "message": "Solicitud encontrada",
            "data": {
                "id": solicitud.id,
                "usuario_id": solicitud.usuario_id,
                "tipo_certificado": solicitud.tipo_certificado,
                "estado": solicitud.estado,
                "comprobante_pago": solicitud.comprobante_pago,
                "fecha_solicitud": solicitud.fecha_solicitud
            }
        }
    
    def cancelar_solicitud(self, solicitud_id: int, usuario_id: int) -> dict:
        solicitud = self.repo.get_by_id(solicitud_id)

        # Regla: la solicitud debe existir
        if not solicitud:
            raise ValueError(
                "No existe una solicitud con el id proporcionado"
            )

        # Regla: debe pertenecer al estudiante
        if solicitud.usuario_id != usuario_id:
            raise PermissionError(
                "No tiene permisos para cancelar esta solicitud"
            )

        # Regla del domain: solo se puede cancelar si está PENDIENTE
        if not solicitud.puede_cancelarse():
            raise ConflictError(
                "Solo se pueden cancelar solicitudes en estado PENDIENTE"
            )

        self.repo.delete(solicitud_id)

        return {
            "success": True,
            "statusCode": 204,
            "message": "Solicitud cancelada correctamente",
            "data": None
        }
    
    def aprobar_rechazar_solicitud(self, solicitud_id: int, data: ActualizarEstadoRequest) -> dict:
        solicitud = self.repo.get_by_id(solicitud_id)

        # Regla: la solicitud debe existir
        if not solicitud:
            raise ValueError("No existe una solicitud con el id proporcionado")

        # Regla: solo se puede gestionar si está PENDIENTE
        if not solicitud.esta_pendiente():
            raise ConflictError("Solo se pueden aprobar o rechazar solicitudes en estado PENDIENTE")

        # Regla: motivo obligatorio si se rechaza
        if data.estado == "RECHAZADA" and not data.motivo_rechazo:
            raise ValueError("El motivo de rechazo es obligatorio")

        self.repo.actualizar_estado(solicitud_id, data.estado, data.motivo_rechazo)

        solicitud = self.repo.get_by_id(solicitud_id)
        mensaje = ("Solicitud aprobada correctamente" if data.estado == "APROBADA" else "Solicitud rechazada correctamente")

        response = {
            "success": True,
            "statusCode": 200,
            "message": mensaje,
            "data": {
                "id": solicitud.id,
                "usuario_id": solicitud.usuario_id,
                "tipo_certificado": solicitud.tipo_certificado,
                "estado": solicitud.estado,
                "fecha_solicitud": solicitud.fecha_solicitud
            }
        }

        if data.estado == "RECHAZADA":
            response["data"]["motivo_rechazo"] = data.motivo_rechazo

        return response

solicitud_service = SolicitudService()