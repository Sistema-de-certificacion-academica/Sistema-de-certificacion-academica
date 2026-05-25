from pydantic import BaseModel, ConfigDict, Field, field_validator
import re

EMAIL_REGEX = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
ROLES_PERMITIDOS = frozenset({"ESTUDIANTE", "ADMINISTRADOR", "EMPRESA_EXTERNA"})

class User:
    def __init__(self, id: int, nombre: str, correo: str, password: str, rol: str, 
                 activo: bool = True, bloqueado: bool = False, intentos_fallidos: int = 0):
        self.id = id
        self.nombre = nombre
        self.correo = correo
        self.password = password
        self.rol = rol
        self.activo = activo
        self.bloqueado = bloqueado
        self.intentos_fallidos = intentos_fallidos
    
    def esta_bloqueado(self) -> bool:
        return self.bloqueado

    def supero_intentos(self, max_intentos: int = 5) -> bool:
        return self.intentos_fallidos >= max_intentos

    def intentos_restantes(self, max_intentos: int = 5) -> int:
        return max_intentos - self.intentos_fallidos

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

    class Config:
        from_attributes = True