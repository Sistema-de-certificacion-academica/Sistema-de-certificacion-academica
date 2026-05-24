import re
from pydantic import BaseModel, ConfigDict, Field, field_validator

EMAIL_REGEX = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
ROLES_PERMITIDOS = frozenset({"ESTUDIANTE", "ADMINISTRADOR", "EMPRESA_EXTERNA"})


# ----------------------------------------------------------------
# Modelos de Dominio
# ----------------------------------------------------------------

class User:
    """Modelo de dominio para usuario"""
    def __init__(self, id: int, nombre: str, correo: str, password: str, rol: str, activo: bool = True):
        self.id = id
        self.nombre = nombre
        self.correo = correo
        self.password = password
        self.rol = rol
        self.activo = activo


# ----------------------------------------------------------------
# Esquemas Pydantic
# ----------------------------------------------------------------

class UserCreate(BaseModel):
    nombre: str = Field(..., min_length=1)
    correo: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)
    rol: str

    @field_validator("correo")
    @classmethod
    def validate_correo(cls, v: str) -> str:
        if not re.match(EMAIL_REGEX, v):
            raise ValueError("El correo electrónico no es válido")
        return v

    @field_validator("rol")
    @classmethod
    def validate_rol(cls, v: str) -> str:
        if v not in ROLES_PERMITIDOS:
            raise ValueError("El rol no es válido")
        return v


class UserResponseData(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    correo: str
    rol: str
    activo: bool


class UserResponse(BaseModel):
    success: bool = True
    statusCode: int = 201
    message: str = "Usuario registrado correctamente"
    data: UserResponseData


class UserDeleteResponse(BaseModel):
    success: bool = True
    statusCode: int = 200
    message: str = "Usuario eliminado correctamente"