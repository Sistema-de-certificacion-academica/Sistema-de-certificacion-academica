from app.verificaciones.repository.verificaciones_repo import verificacion_repository

class VerificacionService:

    def __init__(self):
        self.repo = verificacion_repository

    def registrar_consulta(self, uuid_consultado: str, ip_verificador: str) -> dict:
        verificacion = self.repo.create_verificacion(uuid_consultado, ip_verificador)

        return {
            "success": True,
            "statusCode": 201,
            "message": "Consulta registrada correctamente",
            "data": {
                "id": verificacion.id,
                "uuid_consultado": verificacion.uuid_consultado,
                "ip_verificador": verificacion.ip_verificador,
                "timestamp": verificacion.timestamp
            }
        }

    def listar_consultas(self, uuid: str = None) -> dict:
        verificaciones = self.repo.get_verificaciones(uuid)

        if not verificaciones:
            return {
                "success": True,
                "statusCode": 200,
                "message": "No hay consultas registradas",
                "data": []
            }

        return {
            "success": True,
            "statusCode": 200,
            "message": "Historial de verificaciones encontrado",
            "data": [
                {
                    "id": v.id,
                    "uuid_consultado": v.uuid_consultado,
                    "ip_verificador": v.ip_verificador,
                    "timestamp": v.timestamp
                }
                for v in verificaciones
            ]
        }
    
    def verificar_certificado(self, uuid: str, ip_verificador: str) -> dict:
        if len(uuid) < 8:
            raise ValueError("El formato del UUID no es válido")

        self.registrar_consulta(uuid, ip_verificador)

        certificado = self.repo.get_certificado_by_uuid(uuid)

        if not certificado:
            raise ValueError("No existe un certificado con el UUID proporcionado")

        if certificado.esta_anulado():
            return {
                "success": True,
                "statusCode": 200,
                "message": "Certificado no válido",
                "data": {
                    "valido": False,
                    "uuid": certificado.uuid,
                    "estado": "ANULADO"
                }
            }

        return {
            "success": True,
            "statusCode": 200,
            "message": "Certificado verificado correctamente",
            "data": {
                "valido": True,
                "uuid": certificado.uuid,
                "estudiante": certificado.estudiante,
                "tipo_certificado": certificado.tipo_certificado,
                "fecha_emision": certificado.fecha_emision,
                "estado": "VIGENTE"
            }
        }

verificacion_service = VerificacionService()