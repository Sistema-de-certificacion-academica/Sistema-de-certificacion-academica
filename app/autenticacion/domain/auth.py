from pydantic import BaseModel, Field, field_validator

class LoginRequest(BaseModel):
    correo: str = Field(..., min_length=5)
    password: str = Field(..., min_length=3)

    @field_validator("correo")
    @classmethod
    def correo_valido(cls, v):
        if "@" not in v:
            raise ValueError("El correo no tiene formato válido")
        return v.lower().strip()

    @field_validator("password")
    @classmethod
    def password_sin_espacios(cls, v):
        if " " in v:
            raise ValueError("La contraseña no puede contener espacios")
        return v

ROLES_VALIDOS = frozenset({"ESTUDIANTE", "ADMINISTRADOR", "EMPRESA_EXTERNA"})
