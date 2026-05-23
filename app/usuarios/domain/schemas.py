import re
from pydantic import BaseModel, Field, field_validator

# Expresión regular para validar formato de correo electrónico
EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

class UserCreate(BaseModel):
    nombre: str = Field(..., min_length=1)
    correo: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)
    rol: str

    @field_validator('correo')

    @classmethod

    def validate_correo(cls, v: str) -> str:
        if not re.match(EMAIL_REGEX, v):
            raise ValueError('El correo electrónico no es válido')
        return v

    @field_validator('rol')

    @classmethod
    def validate_rol(cls, v: str) -> str: 
        
        allowed_roles = {"ESTUDIANTE", "ADMINISTRADOR","EMPRESA_EXTERNA"}

        if v not in allowed_roles:
            raise ValueError('El rol no es válido')
        return v

class UserResponseData(BaseModel):
    id: int
    nombre: str
    correo: str
    rol: str
    activo: bool

    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    success: bool = True
    statusCode: int = 201
    message: str = "Usuario registrado correctamente"
    data: UserResponseData