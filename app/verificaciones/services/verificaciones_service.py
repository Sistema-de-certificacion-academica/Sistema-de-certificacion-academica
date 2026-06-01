import hashlib
from typing import Optional
from app.verificaciones.repository.verificaciones_repo import (VerificacionRepository, verificacion_repository)
from app.verificaciones.domain.verificaciones import UUID_REGEX

class UUIDInvalidoError(Exception):
    pass

class VerificacionService:

    def __init__(self, repo: VerificacionRepository):
        self.repo = repo

    def _validar_uuid(self, uuid_str: str) -> None:
        if not UUID_REGEX.match(uuid_str):
            raise UUIDInvalidoError("El formato del UUID no es válido")

    def _registrar_consulta_interna(self, uuid_consultado: str, ip_verificador: str) -> None:
        self.repo.registrar_verificacion(uuid_consultado, ip_verificador)

    def verificar_certificado(self, uuid_str: str, ip_verificador: str) -> dict:
        self._validar_uuid(uuid_str)
        self._registrar_consulta_interna(uuid_str, ip_verificador)

        certificado = self.repo.get_certificado_by_uuid(uuid_str)
        if not certificado:
            raise ValueError("No existe un certificado con el UUID proporcionado")

        if certificado.esta_anulado():
            return certificado.to_verificacion_anulada()

        return certificado.to_verificacion_valida()

    def listar_consultas(self, uuid: Optional[str] = None) -> list:
        verificaciones = self.repo.get_verificaciones(uuid)
        return [v.to_response() for v in verificaciones]

    def validar_integridad(self, uuid_str: str) -> dict:
        self._validar_uuid(uuid_str)

        certificado = self.repo.get_certificado_by_uuid(uuid_str)
        if not certificado:
            raise ValueError("No existe un certificado con el UUID proporcionado")

        # Simula recalcular el hash del PDF
        nombre_clave = certificado.estudiante.split()[0].lower()
        hash_recalculado = hashlib.sha256(f"certificado_{nombre_clave}".encode()).hexdigest()

        integro = certificado.verificar_integridad(hash_recalculado)
        return certificado.to_integridad(integro)

verificacion_service = VerificacionService(repo=verificacion_repository)