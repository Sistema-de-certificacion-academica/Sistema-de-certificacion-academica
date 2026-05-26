import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from app.autenticacion.api.auth_router import router as auth_router
from app.usuarios.api.router import router as usuarios_router
from app.solicitudes.api.solicitudes_router import router as solicitudes_router

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
    allow_headers=["*"],
)

@app.exception_handler(HTTPException)
def http_exception_handler(request, exc: HTTPException):
    error_codes = {
        400: "BAD_REQUEST",
        401: "UNAUTHORIZED",
        403: "FORBIDDEN",
        404: "NOT_FOUND",
        409: "CONFLICT",
    }
    error_code = error_codes.get(exc.status_code, "INTERNAL_SERVER_ERROR")
    message = "No fue posible procesar la solicitud"
    if exc.status_code == 401:
        message = "No autorizado"
    elif exc.status_code == 403:
        message = "Acceso denegado"

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "statusCode": exc.status_code,
            "message": message,
            "error": {
                "error_code": error_code,
                "details": exc.detail,
                "timestamp": datetime.utcnow().isoformat() + "Z",
            },
        },
    )

@app.exception_handler(RequestValidationError)
def validation_exception_handler(request, exc: RequestValidationError):
    errors = exc.errors()
    details_list = []
    for err in errors:
        loc = err.get("loc", [])
        field_path = " -> ".join(str(l) for l in loc if l != "body")
        msg = err.get("msg", "")
        if "field required" in msg or "is missing" in msg:
            details_list.append(f"El campo '{field_path}' es obligatorio")
        else:
            details_list.append(f"El campo '{field_path}': {msg}")
    details_str = "; ".join(details_list) if details_list else "Datos de entrada inválidos"

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "success": False,
            "statusCode": 400,
            "message": "No fue posible procesar la solicitud",
            "error": {
                "error_code": "BAD_REQUEST",
                "details": details_str,
                "timestamp": datetime.utcnow().isoformat() + "Z",
            },
        },
    )

app.include_router(auth_router)
app.include_router(usuarios_router)
app.include_router(solicitudes_router)

@app.get("/")
def root():
    return {"message": "UniCert API funcionando"}