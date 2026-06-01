from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from typing import Optional
from app.core.dependencies import require_estudiante, require_estudiante_o_admin, require_admin
from app.core.responses import success_response, error_response
from app.solicitudes.domain.solicitudes import SolicitudCreate, ActualizarEstadoRequest
from app.solicitudes.services.solicitudes_service import (solicitud_service, ConflictError, PermisoError, MotivoRequeridoError)

router = APIRouter(prefix="/api/v1/solicitudes", tags=["Solicitudes"])

@router.post("", status_code=status.HTTP_201_CREATED)
def crear_solicitud(data: SolicitudCreate, current_user: dict = Depends(require_estudiante)):
    try:
        usuario_id = current_user.get("id")
        data_response = solicitud_service.crear_solicitud(usuario_id, data)
        return success_response(201, "Solicitud creada correctamente", data_response)
    except ConflictError as e:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=error_response(409, "No fue posible crear la solicitud", "CONFLICT", str(e))
        )

@router.get("", status_code=status.HTTP_200_OK)
def listar_solicitudes(estado: Optional[str] = None, current_user: dict = Depends(require_admin)):
    try:
        data = solicitud_service.listar_solicitudes(estado)
        msg = "Solicitudes encontradas" if data else "No hay solicitudes registradas"
        return success_response(200, msg, data)
    except ValueError as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=error_response(400, "No fue posible listar las solicitudes", "BAD_REQUEST", str(e))
        )

@router.get("/{solicitud_id}", status_code=status.HTTP_200_OK)
def consultar_solicitud(solicitud_id: int, current_user: dict = Depends(require_estudiante_o_admin)):
    try:
        usuario_id = current_user.get("id")
        rol = current_user.get("rol")
        data = solicitud_service.consultar_solicitud(solicitud_id, usuario_id, rol)
        return success_response(200, "Solicitud encontrada", data)
    except PermisoError as e:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content=error_response(403, "Acceso denegado", "FORBIDDEN", str(e))
        )
    except ValueError as e:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=error_response(404, "No fue posible consultar la solicitud", "NOT_FOUND", str(e))
        )

@router.delete("/{solicitud_id}", status_code=status.HTTP_200_OK)
def cancelar_solicitud(solicitud_id: int, current_user: dict = Depends(require_estudiante)):
    try:
        usuario_id = current_user.get("id")
        solicitud_service.cancelar_solicitud(solicitud_id, usuario_id)
        return success_response(200, "Solicitud cancelada correctamente", None)
    except PermisoError as e:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content=error_response(403, "Acceso denegado", "FORBIDDEN", str(e))
        )
    except ConflictError as e:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=error_response(409, "No fue posible cancelar la solicitud", "CONFLICT", str(e))
        )
    except ValueError as e:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=error_response(404, "No fue posible cancelar la solicitud", "NOT_FOUND", str(e))
        )

@router.put("/{solicitud_id}/estado", status_code=status.HTTP_200_OK)
def aprobar_rechazar_solicitud(solicitud_id: int, data: ActualizarEstadoRequest, current_user: dict = Depends(require_admin)):
    try:
        data_response = solicitud_service.aprobar_rechazar_solicitud(solicitud_id, data)
        estado = data.estado
        msg = "Solicitud aprobada correctamente" if estado == "APROBADA" else "Solicitud rechazada correctamente"
        return success_response(200, msg, data_response)
    except MotivoRequeridoError as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=error_response(400, "No fue posible actualizar la solicitud", "BAD_REQUEST", str(e))
        )
    except ConflictError as e:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=error_response(409, "No fue posible actualizar la solicitud", "CONFLICT", str(e))
        )
    except ValueError as e:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=error_response(404, "No fue posible actualizar la solicitud", "NOT_FOUND", str(e))
        )