import sys
import os
from datetime import datetime, timezone
sys.path.insert(0, os.path.dirname(__file__))

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from app.autenticacion.api.auth_router import router as auth_router
from app.usuarios.api.router import router as usuarios_router
from app.solicitudes.api.solicitudes_router import router as solicitudes_router
from app.plantillas.api.plantillas_router import router as plantillas_router
from app.certificados.api.certificados_router import router as certificados_router
from app.repositorio.api.repositorio_router import router as repositorio_router
from app.verificaciones.api.verificaciones_router import router as verificaciones_router

app = FastAPI(
    title="UniCert API",
    description="Sistema de Certificación Académica Digital",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

ERROR_CODES = {
    400: "BAD_REQUEST",
    401: "UNAUTHORIZED",
    403: "FORBIDDEN",
    404: "NOT_FOUND",
    409: "CONFLICT",
}

MESSAGES = {
    401: "No autenticado",
    403: "Acceso denegado",
}

@app.exception_handler(HTTPException)
def http_exception_handler(request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "statusCode": exc.status_code,
            "message": MESSAGES.get(exc.status_code, "No fue posible procesar la solicitud"),
            "error": {
                "error_code": ERROR_CODES.get(exc.status_code, "INTERNAL_SERVER_ERROR"),
                "details": exc.detail,
                "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            },
        },
    )

@app.exception_handler(RequestValidationError)
def validation_exception_handler(request, exc: RequestValidationError):
    details_list = []
    for err in exc.errors():
        loc = err.get("loc", [])
        field_path = " -> ".join(str(l) for l in loc if l != "body")
        error_type = err.get("type", "")

        if error_type == "missing":
            details_list.append(f"El campo '{field_path}' es obligatorio")
        elif error_type == "string_too_short":
            details_list.append(f"El campo '{field_path}' no puede estar vacío")
        elif error_type == "value_error":
            details_list.append(f"El campo '{field_path}': {err.get('msg', '').replace('Value error, ', '')}")
        else:
            details_list.append(f"El campo '{field_path}': {err.get('msg', '')}")

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "success": False,
            "statusCode": 400,
            "message": "No fue posible procesar la solicitud",
            "error": {
                "error_code": "BAD_REQUEST",
                "details": "; ".join(details_list) or "Datos de entrada inválidos",
                "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            },
        },
    )

app.include_router(auth_router)
app.include_router(usuarios_router)
app.include_router(solicitudes_router)
app.include_router(verificaciones_router)
app.include_router(plantillas_router)
app.include_router(certificados_router)
app.include_router(repositorio_router)

@app.get("/")
def root():
    return {"message": "UniCert API funcionando"}