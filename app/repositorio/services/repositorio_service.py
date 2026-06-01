from app.repositorio.repository.repositorio_repo import (RepositorioRepository, repositorio_repository)
from app.repositorio.domain.repositorio import UUID_REGEX

class CertificadoAnuladoError(Exception):
    pass

class AccesoDenegadoError(Exception):
    pass

class UUIDInvalidoError(Exception):
    pass

class RepositorioService:

    def __init__(self, repo: RepositorioRepository):
        self.repo = repo

    def _validar_uuid(self, uuid_str: str) -> None:
        if not UUID_REGEX.match(uuid_str):
            raise UUIDInvalidoError("El formato del UUID no es válido")

    def buscar_certificado_por_uuid(self, uuid_str: str, usuario_id: int, rol: str) -> dict:
        certificado = self.repo.get_by_uuid(uuid_str)
        if not certificado:
            raise ValueError("No existe un certificado con el UUID proporcionado")

        if rol == "ESTUDIANTE" and not certificado.pertenece_a(usuario_id):
            raise AccesoDenegadoError("No tiene permisos para consultar este certificado")

        if not certificado.tiene_estado_valido():
            raise RuntimeError(f"Estado de certificado inválido: {certificado.estado}")

        return certificado.to_response()

    def obtener_historial_estudiante(self, estudiante_id: int, usuario_id: int, rol: str) -> list:
        if rol == "ESTUDIANTE" and estudiante_id != usuario_id:
            raise AccesoDenegadoError("No tiene permisos para consultar este historial")

        certificados = self.repo.get_by_usuario_id(estudiante_id)
        return [c.to_history_item() for c in certificados]

    def obtener_metadatos_publicos(self, uuid_str: str) -> dict:
        self._validar_uuid(uuid_str)

        certificado = self.repo.get_by_uuid(uuid_str)
        if not certificado:
            raise ValueError("No existe un certificado con el UUID proporcionado")

        return certificado.to_metadata()

    def descargar_pdf_certificado(self, uuid_str: str, usuario_id: int, rol: str) -> bytes:
        certificado = self.repo.get_by_uuid(uuid_str)
        if not certificado:
            raise ValueError("No existe un certificado con el UUID proporcionado")

        if certificado.esta_anulado():
            raise CertificadoAnuladoError("El certificado está anulado y no puede descargarse")

        if rol == "ESTUDIANTE" and not certificado.pertenece_a(usuario_id):
            raise AccesoDenegadoError("No tiene permisos para descargar este certificado")

        return self._generar_pdf_simulado(uuid_str)  

    def _generar_pdf_simulado(self, uuid: str) -> bytes:
        contenido = f"Certificado UUID: {uuid}\nDocumento simulado."
        return (
            b"%PDF-1.4\n"
            b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n"
            b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n"
            b"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792]\n"
            b"   /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>\nendobj\n"
            b"4 0 obj\n<< /Length 90 >>\nstream\n"
            b"BT /F1 12 Tf 72 720 Td "
            + f"({contenido})".encode()
            + b" Tj ET\nendstream\nendobj\n"
            b"5 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n"
            b"xref\n0 6\n"
            b"0000000000 65535 f \n"
            b"trailer\n<< /Size 6 /Root 1 0 R >>\nstartxref\n0\n%%EOF"
        )

repositorio_service = RepositorioService(repo=repositorio_repository)