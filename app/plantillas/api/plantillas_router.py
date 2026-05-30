from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from app.core.dependencies import require_admin
from app.core.responses import success_response, error_response
from app.plantillas.domain.plantillas import PlantillaCreate, PlantillaUpdate
from app.plantillas.services.plantillas_service import (plantilla_service, TipoInvalidoError, PlantillaUsadaError)

router = APIRouter(prefix="/api/v1/plantillas", tags=["Plantillas"])

@router.post("", status_code=status.HTTP_201_CREATED)
def crear_plantilla(data: PlantillaCreate, current_user: dict = Depends(require_admin)):
    try:
        data_response = plantilla_service.crear_plantilla(data)
        return success_response(201, "Plantilla creada correctamente", data_response)
    except TipoInvalidoError as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=error_response(400, "No fue posible crear la plantilla", "BAD_REQUEST", str(e))
        )
    except ValueError as e:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=error_response(409, "No fue posible crear la plantilla", "CONFLICT", str(e))
        )

@router.get("", status_code=status.HTTP_200_OK)
def listar_plantillas(current_user: dict = Depends(require_admin)):
    data = plantilla_service.listar_plantillas()
    msg = "Plantillas encontradas" if data else "No hay plantillas registradas en el sistema"
    return success_response(200, msg, data)


@router.put("/{plantilla_id}", status_code=status.HTTP_200_OK)
def editar_plantilla(plantilla_id: int, data: PlantillaUpdate, current_user: dict = Depends(require_admin)):
    try:
        data_response = plantilla_service.editar_plantilla(plantilla_id, data)
        return success_response(200, "Plantilla actualizada correctamente", data_response)
    except TipoInvalidoError as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=error_response(400, "No fue posible editar la plantilla", "BAD_REQUEST", str(e))
        )
    except PlantillaUsadaError as e:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=error_response(409, "No fue posible editar la plantilla", "CONFLICT", str(e))
        )
    except ValueError as e:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=error_response(404, "No fue posible editar la plantilla", "NOT_FOUND", str(e))
        )