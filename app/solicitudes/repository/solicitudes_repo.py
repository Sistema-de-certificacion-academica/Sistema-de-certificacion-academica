from typing import Optional
from app.solicitudes.domain.solicitudes import Solicitud, SolicitudCreate

class SolicitudRepository:
    _solicitudes: list[Solicitud] = []
    _siguiente_id: int = 1

    def get_by_id(self, solicitud_id: int) -> Optional[Solicitud]:
        for s in self._solicitudes:
            if s.id == solicitud_id:
                return s
        return None

    def get_by_usuario_y_tipo(self, usuario_id: int, tipo_certificado: str) -> Optional[Solicitud]:
        for s in self._solicitudes:
            if (s.usuario_id == usuario_id and
                    s.tipo_certificado == tipo_certificado and
                    s.estado == "PENDIENTE"):
                return s
        return None

    def get_by_usuario(self, usuario_id: int) -> list[Solicitud]:
        return [s for s in self._solicitudes if s.usuario_id == usuario_id]

    def get_all(self, estado: str = None) -> list[Solicitud]:
        if estado:
            return [s for s in self._solicitudes if s.estado == estado]
        return self._solicitudes.copy()

    def create(self, usuario_id: int, data: SolicitudCreate) -> Solicitud:
        solicitud = Solicitud(
            id=type(self)._siguiente_id,
            usuario_id=usuario_id,
            tipo_certificado=data.tipo_certificado,
            comprobante_pago=data.comprobante_pago
        )
        type(self)._solicitudes.append(solicitud)
        type(self)._siguiente_id += 1
        return solicitud

    def actualizar_estado(self, solicitud_id: int, nuevo_estado: str,
                          motivo_rechazo: str = None) -> Optional[Solicitud]:
        solicitud = self.get_by_id(solicitud_id)
        if solicitud:
            solicitud.estado = nuevo_estado
            if motivo_rechazo:
                solicitud.motivo_rechazo = motivo_rechazo
        return solicitud

    def delete(self, solicitud_id: int) -> bool:
        for i, s in enumerate(self._solicitudes):
            if s.id == solicitud_id:
                self._solicitudes.pop(i)
                return True
        return False

solicitud_repository = SolicitudRepository()