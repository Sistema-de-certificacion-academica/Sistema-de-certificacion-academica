from datetime import datetime, timedelta, timezone
from app.usuarios.repository.usuario_repo import UserRepository

MAX_INTENTOS = 5
MINUTOS_BLOQUEO = 15

class AuthRepository:

    def __init__(self):
        self._user_repo = UserRepository()
        self._tokens_invalidados: set = set()

    def get_by_correo(self, correo: str):
        return self._user_repo.get_by_correo(correo)

    def actualizar_intentos(self, correo: str, intentos: int) -> None:
        usuario = self.get_by_correo(correo)
        if usuario:
            usuario.intentos_fallidos = intentos

    def bloquear_usuario(self, correo: str) -> None:
        usuario = self.get_by_correo(correo)
        if usuario:
            usuario.bloqueado_hasta = datetime.now(timezone.utc) + timedelta(minutes=MINUTOS_BLOQUEO)
            usuario.intentos_fallidos = 0

    def resetear_intentos(self, correo: str) -> None:
        usuario = self.get_by_correo(correo)
        if usuario:
            usuario.intentos_fallidos = 0
            usuario.bloqueado_hasta = None

    def invalidar_token(self, token: str) -> bool:
        if token in self._tokens_invalidados:
            return False
        self._tokens_invalidados.add(token)
        return True

    def token_es_invalido(self, token: str) -> bool:
        return token in self._tokens_invalidados

auth_repository = AuthRepository()