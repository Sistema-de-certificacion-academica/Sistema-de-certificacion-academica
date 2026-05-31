from typing import Optional
from uuid import uuid4

from app.certificados.domain.certificados import Certificate


class CertificateRepository:

    def __init__(self):
        self._certificados: list[Certificate] = []
        self._next_id: int = 1
        self._seed()

    def _seed(self):
        """Carga certificados de prueba con informacion de estudiantes."""
        iniciales = [
            Certificate(
                id=1,
                uuid=str(uuid4()),
                solicitud_id=1,
                plantilla_id=1,
                estado="GENERADO",
                fecha_emision="2026-03-18T10:00:00Z",
                nombre_estudiante="Erick Gutierrez",
                programa_academico="Tecnologia en Sistemas",
            ),
            Certificate(
                id=2,
                uuid=str(uuid4()),
                solicitud_id=2,
                plantilla_id=1,
                estado="GENERADO",
                fecha_emision="2026-02-10T09:30:00Z",
                nombre_estudiante="Hansel Rodriguez",
                programa_academico="Ingenieria de Software",
            ),
            Certificate(
                id=3,
                uuid=str(uuid4()),
                solicitud_id=3,
                plantilla_id=1,
                estado="GENERADO",
                fecha_emision="2026-01-15T14:20:00Z",
                nombre_estudiante="Carlos Perez",
                programa_academico="Administracion de Sistemas",
            ),
        ]
        self._certificados = iniciales
        self._next_id = 4

    def obtener_todos(self) -> list[Certificate]:
        return self._certificados.copy()

    def obtener_por_id(self, id: int) -> Optional[Certificate]:
        return next((c for c in self._certificados if c.id == id), None)

    def obtener_por_uuid(self, uuid: str) -> Optional[Certificate]:
        return next((c for c in self._certificados if c.uuid == uuid), None)

    def crear(self, solicitud_id: int, plantilla_id: int, uuid: str,
              fecha_emision: str, estado: str = "GENERADO",
              ruta_pdf: str = None) -> Certificate:
        certificado = Certificate(
            id=self._next_id,
            uuid=uuid,
            solicitud_id=solicitud_id,
            plantilla_id=plantilla_id,
            estado=estado,
            fecha_emision=fecha_emision,
            ruta_pdf=ruta_pdf,
        )
        self._certificados.append(certificado)
        self._next_id += 1
        return certificado

    def actualizar_estado(self, id: int, nuevo_estado: str) -> Optional[Certificate]:
        certificado = self.obtener_por_id(id)
        if not certificado:
            return None
        certificado.estado = nuevo_estado
        return certificado


certificate_repository = CertificateRepository()
