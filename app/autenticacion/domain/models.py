from pydantic import BaseModel
from typing import Optional

# Request q recibe el login
class LoginRequest(BaseModel):
    correo: str
    password: str

# Datos del usuario dentro del token
class UsuarioToken(BaseModel):
    id: int
    nombre: str
    correo: str
    rol: str

# Response login ok
class LoginResponse(BaseModel):
    success: bool
    statusCode: int
    message: str
    data: dict

# Response error 
class ErrorResponse(BaseModel):
    success: bool
    statusCode: int
    message: str
    error: dict