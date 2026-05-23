# app/autenticacion/repository/auth_repository.py
# ─────────────────────────────────────────────────
# CAPA REPOSITORIO — acceso a datos de autenticación
# Solo guarda y recupera datos
# Sin lógica de negocio
# Sin imports de FastAPI
# ─────────────────────────────────────────────────

from typing import Optional
from app.autenticacion.domain.auth import Login
from app.core.security import hash_password


class AuthRepository:

    def __init__(self):
        # Lista en memoria — temporal hasta que
        # tu compañero termine el módulo usuarios
        self._usuarios: list[Login] = []
        self._siguiente_id: int = 1
        self._seed()

    def _seed(self):
        """Usuarios de prueba para desarrollo."""
        usuarios_prueba = [
            Login(
                id=1,
                nombre="Admin UniCert",
                correo="admin@unicert.com",
                password_hash=hash_password("admin123"),
                rol="ADMINISTRADOR"
            ),
            Login(
                id=2,
                nombre="Erick Gutierrez",
                correo="erick@unicert.com",
                password_hash=hash_password("erick123"),
                rol="ESTUDIANTE"
            )
        ]
        self._usuarios = usuarios_prueba
        self._siguiente_id = 3

    def get_by_correo(
        self,
        correo: str
    ) -> Optional[Login]:
        """
        Busca usuario por correo.
        Retorna None si no existe.
        """
        return next(
            (u for u in self._usuarios
             if u.correo == correo),
            None
        )

    def actualizar_intentos(
        self,
        correo: str,
        intentos: int
    ) -> None:
        """Actualiza contador de intentos fallidos."""
        usuario = self.get_by_correo(correo)
        if usuario:
            usuario.intentos_fallidos = intentos

    def bloquear_usuario(
        self,
        correo: str
    ) -> None:
        """Bloquea usuario al superar intentos máximos."""
        usuario = self.get_by_correo(correo)
        if usuario:
            usuario.bloqueado = True
            usuario.intentos_fallidos = 0

    def resetear_intentos(
        self,
        correo: str
    ) -> None:
        """Resetea intentos tras login exitoso."""
        usuario = self.get_by_correo(correo)
        if usuario:
            usuario.intentos_fallidos = 0


# Instancia única compartida como el profe
auth_repository = AuthRepository()