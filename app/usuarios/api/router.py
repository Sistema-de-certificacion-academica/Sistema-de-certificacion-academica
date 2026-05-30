from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from app.core.dependencies import require_admin
from app.core.responses import success_response, error_response
from app.usuarios.domain.usuarios import UserCreate, UserUpdate
from app.usuarios.services.usuario_service import (
    usuario_services, ConflictError, RolInvalidoError, AutoeliminacionError
)
from typing import Optional

router = APIRouter(prefix="/api/v1/usuarios", tags=["Usuarios"])


@router.post("", status_code=status.HTTP_201_CREATED)
def registrar_usuario(user_data: UserCreate, current_user: dict = Depends(require_admin)):
    try:
        data = usuario_services.registrar_usuario(user_data)
        return success_response(201, "Usuario registrado correctamente", data)
    except ConflictError as e:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=error_response(409, "No fue posible registrar el usuario", "CONFLICT", str(e))
        )

@router.post("/registro", status_code=status.HTTP_201_CREATED)
def registro_estudiante(user_data: UserCreate):
    try:
        data = usuario_services.registrar_estudiante(user_data)
        return success_response(201, "Usuario registrado correctamente", data)
    except RolInvalidoError as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=error_response(400, "No fue posible registrar el usuario", "BAD_REQUEST", str(e))
        )
    except ConflictError as e:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=error_response(409, "No fue posible registrar el usuario", "CONFLICT", str(e))
        )


@router.get("", status_code=status.HTTP_200_OK)
def listar_usuarios(rol: Optional[str] = None, current_user: dict = Depends(require_admin)):
    try:
        data = usuario_services.listar_usuarios(rol)
        msg = "Usuarios encontrados" if data else "No hay usuarios registrados en el sistema"
        return success_response(200, msg, data)
    except ValueError as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=error_response(400, "No fue posible listar los usuarios", "BAD_REQUEST", str(e))
        )


@router.get("/{usuario_id}", status_code=status.HTTP_200_OK)
def consultar_usuario(usuario_id: int, current_user: dict = Depends(require_admin)):
    try:
        data = usuario_services.obtener_usuario_por_id(usuario_id)
        return success_response(200, "Usuario encontrado", data)
    except ValueError as e:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=error_response(404, "No fue posible consultar el usuario", "NOT_FOUND", str(e))
        )

@router.put("/{usuario_id}", status_code=status.HTTP_200_OK)
def actualizar_usuario(usuario_id: int, user_data: UserUpdate, current_user: dict = Depends(require_admin)):
    try:
        data = usuario_services.actualizar_perfil_usuario(usuario_id, user_data)
        return success_response(200, "Usuario actualizado correctamente", data)
    except ConflictError as e:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=error_response(409, "No fue posible actualizar el usuario", "CONFLICT", str(e))
        )
    except RolInvalidoError as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=error_response(400, "No fue posible actualizar el usuario", "BAD_REQUEST", str(e))
        )
    except ValueError as e:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=error_response(404, "No fue posible actualizar el usuario", "NOT_FOUND", str(e))
        )


@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
def eliminar_usuario(user_id: int, current_user: dict = Depends(require_admin)):
    try:
        admin_id = current_user.get("id")
        usuario_services.eliminar_usuario(user_id, admin_id)
        return success_response(200, "Usuario eliminado correctamente", None)
    except AutoeliminacionError as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=error_response(400, "No fue posible eliminar el usuario", "BAD_REQUEST", str(e))
        )
    except ConflictError as e:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=error_response(409, "No fue posible eliminar el usuario", "CONFLICT", str(e))
        )
    except ValueError as e:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=error_response(404, "No fue posible eliminar el usuario", "NOT_FOUND", str(e))
        )