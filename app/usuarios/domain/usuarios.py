from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator
import re
from datetime import datetime

EMAIL_REGEX = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
ROLES_PERMITIDOS = frozenset({"ESTUDIANTE", "ADMINISTRADOR", "EMPRESA_EXTERNA"})
ROLES_ACTUALIZABLES = frozenset({"ESTUDIANTE", "ADMINISTRADOR"})

class User:
    def __init__(self, id: int, nombre: str, correo: str, password: str,
                 rol: str, activo: bool = True, bloqueado_hasta: datetime = None, intentos_fallidos: int = 0):
        self.id = id
        self.nombre = nombre
        self.correo = correo
        self.password = password
        self.rol = rol
        self.activo = activo
        self.bloqueado_hasta = bloqueado_hasta
        self.intentos_fallidos = intentos_fallidos

    def esta_bloqueado(self) -> bool:
        if self.bloqueado_hasta is None:
            return False
        return datetime.utcnow() < self.bloqueado_hasta

    def supero_intentos(self, max_intentos: int = 5) -> bool:
        return self.intentos_fallidos >= max_intentos

    def intentos_restantes(self, max_intentos: int = 5) -> int:
        return max_intentos - self.intentos_fallidos
    
    def to_response(self) -> dict:        
        return {
            "id": self.id,
            "nombre": self.nombre,
            "correo": self.correo,
            "rol": self.rol,
            "activo": self.activo
        }
    
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

class UserResponse(BaseModel):
    id: int
    nombre: str
    correo: str
    rol: str
    activo: bool

class UserUpdate(BaseModel):
    model_config = ConfigDict(extra='ignore')

    nombre: Optional[str] = Field(None, min_length=1)
    correo: Optional[str] = Field(None, min_length=1)
    rol: Optional[str] = None

    @field_validator("correo", mode="before")
    @classmethod
    def validate_correo(cls, v):
        if v is None:
            return v
        if not re.match(EMAIL_REGEX, v):
            raise ValueError("El correo electrónico no es válido")
        return v
