from typing import Optional
from app.certificados.domain.certificados import Certificate, CertificateCreate
from uuid import uuid4

class CertificateRepository:
    _certificados: list[Certificate] = []
    _next_id: int = 1
    _seeded: bool = False

    def __init__(self):
        if not type(self)._seeded:
            self._seed()
            type(self)._seeded = True

    def _seed(self):
        """Crear certificados de prueba con información de estudiantes"""
        certificados_prueba = [
            Certificate(
                id=type(self)._next_id,
                uuid=str(uuid4()),
                solicitud_id=1,
                plantilla_id=1,
                estado="GENERADO",
                fecha_emision="2026-03-18T10:00:00Z",
                nombre_estudiante="Erick Gutierrez",
                programa_academico="Tecnología en Sistemas"
            ),
            Certificate(
                id=type(self)._next_id + 1,
                uuid=str(uuid4()),
                solicitud_id=2,
                plantilla_id=1,
                estado="GENERADO",
                fecha_emision="2026-02-10T09:30:00Z",
                nombre_estudiante="Hansel Rodriguez",
                programa_academico="Ingeniería de Software"
            ),
            Certificate(
                id=type(self)._next_id + 2,
                uuid=str(uuid4()),
                solicitud_id=3,
                plantilla_id=1,
                estado="GENERADO",
                fecha_emision="2026-01-15T14:20:00Z",
                nombre_estudiante="Carlos Perez",
                programa_academico="Administración de Sistemas"
            ),
        ]
        type(self)._certificados.extend(certificados_prueba)
        type(self)._next_id += 3

    def save(self, data: CertificateCreate, uuid: str, fecha_emision: str, estado: str = "GENERADO") -> Certificate:
        certificado = Certificate(
            id=type(self)._next_id,
            uuid=uuid,
            solicitud_id=data.solicitud_id,
            plantilla_id=data.plantilla_id,
            estado=estado,
            fecha_emision=fecha_emision
        )
        self._certificados.append(certificado)
        type(self)._next_id += 1
        return certificado

    def get_by_id(self, id: int) -> Optional[Certificate]:
        for c in self._certificados:
            if c.id == id:
                return c
        return None

    def get_by_uuid(self, uuid: str) -> Optional[Certificate]:
        for c in self._certificados:
            if c.uuid == uuid:
                return c
        return None

    def update_estado(self, id: int, nuevo_estado: str) -> Optional[Certificate]:
        for c in self._certificados:
            if c.id == id:
                c.estado = nuevo_estado
                return c
        return None

certificate_repository = CertificateRepository()
