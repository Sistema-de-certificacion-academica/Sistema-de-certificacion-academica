from app.solicitudes.repository.solicitudes_repo import SolicitudRepository, solicitud_repository
from app.solicitudes.domain.solicitudes import SolicitudCreate, ActualizarEstadoRequest, ESTADOS_SOLICITUD

class ConflictError(Exception):
    pass

class PermisoError(Exception):
    pass

class MotivoRequeridoError(ValueError):
    pass

class SolicitudService:

    def __init__(self, repo: SolicitudRepository):
        self.repo = repo

    def crear_solicitud(self, usuario_id: int, data: SolicitudCreate) -> dict:
        existente = self.repo.get_by_usuario_y_tipo(usuario_id, data.tipo_certificado)
        if existente:
            raise ConflictError("Ya tienes una solicitud pendiente de ese tipo de certificado")
        solicitud = self.repo.create(usuario_id, data)
        return solicitud.to_response()

    def consultar_solicitud(self, solicitud_id: int, usuario_id: int, rol: str) -> dict:
        solicitud = self.repo.get_by_id(solicitud_id)
        if not solicitud:
            raise ValueError("No existe una solicitud con el id proporcionado")
        if rol == "ESTUDIANTE" and solicitud.usuario_id != usuario_id:
            raise PermisoError("No tiene permisos para consultar esta solicitud")
        return solicitud.to_response()

    def cancelar_solicitud(self, solicitud_id: int, usuario_id: int) -> None:
        solicitud = self.repo.get_by_id(solicitud_id)
        if not solicitud:
            raise ValueError("No existe una solicitud con el id proporcionado")
        if solicitud.usuario_id != usuario_id:
            raise PermisoError("No tiene permisos para cancelar esta solicitud")
        if not solicitud.puede_cancelarse():
            raise ConflictError("Solo se pueden cancelar solicitudes en estado PENDIENTE")
        self.repo.delete(solicitud_id)

    def aprobar_rechazar_solicitud(self, solicitud_id: int, data: ActualizarEstadoRequest) -> dict:
        solicitud = self.repo.get_by_id(solicitud_id)
        if not solicitud:
            raise ValueError("No existe una solicitud con el id proporcionado")
        if not solicitud.esta_pendiente():
            raise ConflictError("Solo se pueden aprobar o rechazar solicitudes en estado PENDIENTE")
        if data.estado == "RECHAZADA" and not data.motivo_rechazo:
            raise MotivoRequeridoError("El motivo de rechazo es obligatorio")
        
        motivo = data.motivo_rechazo if data.estado == "RECHAZADA" else None
        self.repo.actualizar_estado(solicitud_id, data.estado, motivo)
        solicitud = self.repo.get_by_id(solicitud_id)
        return solicitud.to_response_gestion()

    def listar_solicitudes(self, estado: str = None) -> list:
        if estado and estado not in ESTADOS_SOLICITUD:
            raise ValueError("El estado proporcionado no es válido")
        return [s.to_response() for s in self.repo.get_all(estado)]

    def listar_mis_solicitudes(self, usuario_id: int) -> list:
        return [s.to_response() for s in self.repo.get_by_usuario(usuario_id)]

solicitud_service = SolicitudService(repo=solicitud_repository)