from sqlalchemy.orm import Session
from typing import Optional

class AuthRepository:

    # Busca usuario por correo en lq db
    def get_usuario_por_correo(self, correo: str, db: Session) -> Optional[dict]:
        from usuarios.domain.models import UsuarioModel
        return db.query(UsuarioModel).filter(
            UsuarioModel.correo == correo
        ).first()
    
    # Actualiza intentos fallidos
    def actualizar_intentos_fallidos(self, correo: str, intentos: int, db: Session) -> None:
        from usuarios.domain.models import UsuarioModel
        usuario = db.query(UsuarioModel).filter(
            UsuarioModel.correo == correo
        ).first()
        if usuario:
            usuario.intentos_fallidos = intentos
            db.commit()

    # Bloquea al usuario al superar intentos fallidos 
    def bloquear_usuario(self, correo: str, db: Session) -> None:
        from usuarios.domain.models import UsuarioModel
        usuario = db.query(UsuarioModel).filter(
            UsuarioModel.correo == correo
        ).first()
        if usuario:
            usuario.bloqueado = True
            usuario.intentos_fallidos = 0
            db.commit()

    # Reseta intentos fallidos
    def resetear_intentos(self, correo: str, db: Session) -> None:
        from usuarios.domain.models import UsuarioModel
        usuario = db.query(UsuarioModel).filter(
            UsuarioModel.correo == correo
        ).first()
        if usuario:
            usuario.intentos_fallidos = 0
            db.commit()