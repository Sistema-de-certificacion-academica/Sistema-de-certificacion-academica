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

class LoginResponse(BaseModel):
    id: int
    nombre: str
    correo: str
    rol: str

class Login:
    def __init__(self, id, nombre, correo,
                 password_hash, rol,
                 intentos_fallidos=0,
                 bloqueado=False):
        self.id = id
        self.nombre = nombre
        self.correo = correo
        self.password_hash = password_hash
        self.rol = rol
        self.intentos_fallidos = intentos_fallidos
        self.bloqueado = bloqueado

    def esta_bloqueado(self) -> bool:
        return self.bloqueado

    def supero_intentos(self, max_intentos=5) -> bool:
        return self.intentos_fallidos >= max_intentos

    def intentos_restantes(self, max_intentos=5) -> int:
        return max_intentos - self.intentos_fallidos
    
class LogoutResponse(BaseModel):
    success: bool
    statusCode: int
    message: str
    data: None = None

ROLES_VALIDOS = frozenset({"ESTUDIANTE", "ADMINISTRADOR", "EMPRESA_EXTERNA"})

PERMISOS_POR_ROL = {
    "ADMINISTRADOR": [
        "gestionar_usuarios",
        "gestionar_plantillas", 
        "gestionar_solicitudes",
        "gestionar_certificados"
    ],
    "ESTUDIANTE": [
        "crear_solicitud",
        "consultar_solicitud",
        "descargar_certificado",
        "consultar_historial"
    ],
    "EMPRESA_EXTERNA": [
        "verificar_certificado"
    ]
}