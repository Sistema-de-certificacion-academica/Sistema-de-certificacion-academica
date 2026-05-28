import pytest
from app.solicitudes.domain.solicitudes import (
    SolicitudCreate, Solicitud, ActualizarEstadoRequest,
    TIPOS_CERTIFICADO, ESTADOS_SOLICITUD
)
from app.solicitudes.services.solicitudes_service import SolicitudService, ConflictError
from app.solicitudes.repository.solicitudes_repo import SolicitudRepository


class TestSolicitudCreate:
    """Tests para validación de creación de solicitud"""
    
    def test_crear_solicitud_valida(self):
        """✅ Crear una solicitud con datos válidos"""
        data = SolicitudCreate(
            tipo_certificado="CERTIFICADO_ESTUDIO",
            comprobante_pago="REF-123456"
        )
        assert data.tipo_certificado == "CERTIFICADO_ESTUDIO"
        assert data.comprobante_pago == "REF-123456"
    
    def test_comprobante_pago_limpia_espacios(self):
        """✅ El comprobante de pago se limpia automáticamente"""
        data = SolicitudCreate(
            tipo_certificado="CERTIFICADO_NOTAS",
            comprobante_pago="  REF-789  "
        )
        assert data.comprobante_pago == "REF-789"
    
    def test_tipo_certificado_invalido(self):
        """❌ Rechaza tipos de certificado inválidos"""
        with pytest.raises(ValueError, match="Tipo de certificado no válido"):
            SolicitudCreate(
                tipo_certificado="CERTIFICADO_INEXISTENTE",
                comprobante_pago="REF-123"
            )
    
    def test_comprobante_pago_vacio(self):
        """❌ Rechaza comprobante de pago vacío"""
        with pytest.raises(ValueError, match="no puede estar vacío"):
            SolicitudCreate(
                tipo_certificado="CERTIFICADO_ESTUDIO",
                comprobante_pago=""
            )
    
    def test_comprobante_pago_solo_espacios(self):
        """❌ Rechaza comprobante con solo espacios"""
        with pytest.raises(ValueError, match="no puede estar vacío"):
            SolicitudCreate(
                tipo_certificado="CERTIFICADO_ESTUDIO",
                comprobante_pago="   "
            )


class TestSolicitudDomain:
    """Tests para la lógica de dominio"""
    
    def test_solicitud_inicia_en_pendiente(self):
        """✅ Una solicitud nueva inicia en estado PENDIENTE"""
        solicitud = Solicitud(
            id=1,
            usuario_id=101,
            tipo_certificado="CERTIFICADO_ESTUDIO",
            comprobante_pago="REF-001"
        )
        assert solicitud.estado == "PENDIENTE"
        assert solicitud.esta_pendiente() is True
    
    def test_solicitud_puede_cancelarse_si_pendiente(self):
        """✅ Solo se puede cancelar si está PENDIENTE"""
        solicitud = Solicitud(
            id=1,
            usuario_id=101,
            tipo_certificado="CERTIFICADO_ESTUDIO",
            comprobante_pago="REF-001",
            estado="PENDIENTE"
        )
        assert solicitud.puede_cancelarse() is True
    
    def test_solicitud_no_puede_cancelarse_si_aprobada(self):
        """✅ No se puede cancelar si está APROBADA"""
        solicitud = Solicitud(
            id=1,
            usuario_id=101,
            tipo_certificado="CERTIFICADO_ESTUDIO",
            comprobante_pago="REF-001",
            estado="APROBADA"
        )
        assert solicitud.puede_cancelarse() is False


class TestSolicitudRepository:
    """Tests para el repositorio de solicitudes"""
    
    @pytest.fixture(autouse=True)
    def limpiar_repo(self):
        """Limpia el repositorio antes de cada test"""
        repo = SolicitudRepository()
        repo._solicitudes = []
        repo._siguiente_id = 1
        yield
        repo._solicitudes = []
        repo._siguiente_id = 1
    
    def test_crear_solicitud_en_repo(self):
        """✅ Crear una solicitud en el repositorio"""
        repo = SolicitudRepository()
        data = SolicitudCreate(
            tipo_certificado="CERTIFICADO_ESTUDIO",
            comprobante_pago="REF-123"
        )
        solicitud = repo.create(usuario_id=1, data=data)
        
        assert solicitud.id == 1
        assert solicitud.usuario_id == 1
        assert solicitud.tipo_certificado == "CERTIFICADO_ESTUDIO"
        assert solicitud.comprobante_pago == "REF-123"
    
    def test_obtener_solicitud_por_id(self):
        """✅ Obtener solicitud por ID"""
        repo = SolicitudRepository()
        data = SolicitudCreate(
            tipo_certificado="CERTIFICADO_ESTUDIO",
            comprobante_pago="REF-123"
        )
        solicitud_creada = repo.create(usuario_id=1, data=data)
        solicitud_obtenida = repo.get_by_id(solicitud_creada.id)
        
        assert solicitud_obtenida is not None
        assert solicitud_obtenida.id == solicitud_creada.id
    
    def test_obtener_solicitud_inexistente(self):
        """✅ Retorna None si la solicitud no existe"""
        repo = SolicitudRepository()
        solicitud = repo.get_by_id(999)
        assert solicitud is None
    
    def test_auto_incremento_ids(self):
        """✅ Los IDs se incrementan automáticamente"""
        repo = SolicitudRepository()
        data1 = SolicitudCreate(
            tipo_certificado="CERTIFICADO_ESTUDIO",
            comprobante_pago="REF-001"
        )
        data2 = SolicitudCreate(
            tipo_certificado="CERTIFICADO_NOTAS",
            comprobante_pago="REF-002"
        )
        
        sol1 = repo.create(usuario_id=1, data=data1)
        sol2 = repo.create(usuario_id=1, data=data2)
        
        assert sol1.id == 1
        assert sol2.id == 2
    
    def test_obtener_solicitudes_por_usuario(self):
        """✅ Obtener todas las solicitudes de un usuario"""
        repo = SolicitudRepository()
        data1 = SolicitudCreate(tipo_certificado="CERTIFICADO_ESTUDIO", comprobante_pago="REF-001")
        data2 = SolicitudCreate(tipo_certificado="CERTIFICADO_NOTAS", comprobante_pago="REF-002")
        
        repo.create(usuario_id=1, data=data1)
        repo.create(usuario_id=1, data=data2)
        repo.create(usuario_id=2, data=data1)
        
        solicitudes_usuario_1 = repo.get_by_usuario(usuario_id=1)
        assert len(solicitudes_usuario_1) == 2
    
    def test_obtener_por_usuario_y_tipo_pendiente(self):
        """✅ Obtener solicitud pendiente por usuario y tipo"""
        repo = SolicitudRepository()
        data = SolicitudCreate(
            tipo_certificado="CERTIFICADO_ESTUDIO",
            comprobante_pago="REF-123"
        )
        solicitud = repo.create(usuario_id=1, data=data)
        
        encontrada = repo.get_by_usuario_y_tipo(usuario_id=1, tipo_certificado="CERTIFICADO_ESTUDIO")
        
        assert encontrada is not None
        assert encontrada.id == solicitud.id
    
    def test_actualizar_estado_solicitud(self):
        """✅ Actualizar el estado de una solicitud"""
        repo = SolicitudRepository()
        data = SolicitudCreate(
            tipo_certificado="CERTIFICADO_ESTUDIO",
            comprobante_pago="REF-123"
        )
        solicitud = repo.create(usuario_id=1, data=data)
        
        repo.actualizar_estado(solicitud.id, "APROBADA")
        solicitud_actualizada = repo.get_by_id(solicitud.id)
        
        assert solicitud_actualizada.estado == "APROBADA"
    
    def test_eliminar_solicitud(self):
        """✅ Eliminar una solicitud"""
        repo = SolicitudRepository()
        data = SolicitudCreate(
            tipo_certificado="CERTIFICADO_ESTUDIO",
            comprobante_pago="REF-123"
        )
        solicitud = repo.create(usuario_id=1, data=data)
        
        resultado = repo.delete(solicitud.id)
        assert resultado is True
        
        solicitud_eliminada = repo.get_by_id(solicitud.id)
        assert solicitud_eliminada is None


class TestSolicitudService:
    """Tests para la lógica de negocio (Service)"""
    
    @pytest.fixture(autouse=True)
    def limpiar_repo(self):
        """Limpia el repositorio antes de cada test"""
        from app.solicitudes.repository.solicitudes_repo import solicitud_repository
        solicitud_repository._solicitudes = []
        solicitud_repository._siguiente_id = 1
        yield
        solicitud_repository._solicitudes = []
        solicitud_repository._siguiente_id = 1
    
    def test_crear_solicitud_exitosamente(self):
        """✅ Crear una solicitud con éxito"""
        service = SolicitudService()
        data = SolicitudCreate(
            tipo_certificado="CERTIFICADO_ESTUDIO",
            comprobante_pago="REF-123"
        )
        
        response = service.crear_solicitud(usuario_id=1, data=data)
        
        assert response["success"] is True
        assert response["statusCode"] == 201
        assert response["data"]["usuario_id"] == 1
        assert response["data"]["tipo_certificado"] == "CERTIFICADO_ESTUDIO"
        assert response["data"]["comprobante_pago"] == "REF-123"
        assert response["data"]["estado"] == "PENDIENTE"
    
    def test_no_crear_solicitud_duplicada(self):
        """❌ No permite crear solicitud duplicada pendiente"""
        service = SolicitudService()
        data = SolicitudCreate(
            tipo_certificado="CERTIFICADO_ESTUDIO",
            comprobante_pago="REF-123"
        )
        
        # Primera solicitud - OK
        service.crear_solicitud(usuario_id=1, data=data)
        
        # Segunda solicitud del mismo tipo - ERROR
        with pytest.raises(ValueError, match="Ya tienes una solicitud pendiente"):
            service.crear_solicitud(usuario_id=1, data=data)
    
    def test_consultar_solicitud_exitosamente(self):
        """✅ Consultar una solicitud creada"""
        service = SolicitudService()
        data = SolicitudCreate(
            tipo_certificado="CERTIFICADO_ESTUDIO",
            comprobante_pago="REF-123"
        )
        
        response_creacion = service.crear_solicitud(usuario_id=1, data=data)
        solicitud_id = response_creacion["data"]["id"]
        
        response_consulta = service.consultar_solicitud(
            solicitud_id=solicitud_id,
            usuario_id=1,
            rol="ESTUDIANTE"
        )
        
        assert response_consulta["success"] is True
        assert response_consulta["data"]["id"] == solicitud_id
    
    def test_consultar_solicitud_sin_permisos(self):
        """❌ Estudiante no puede consultar solicitud de otro"""
        service = SolicitudService()
        data = SolicitudCreate(
            tipo_certificado="CERTIFICADO_ESTUDIO",
            comprobante_pago="REF-123"
        )
        
        response_creacion = service.crear_solicitud(usuario_id=1, data=data)
        solicitud_id = response_creacion["data"]["id"]
        
        with pytest.raises(PermissionError, match="No tiene permisos"):
            service.consultar_solicitud(
                solicitud_id=solicitud_id,
                usuario_id=2,  # Otro usuario
                rol="ESTUDIANTE"
            )
    
    def test_cancelar_solicitud_exitosamente(self):
        """✅ Cancelar una solicitud pendiente"""
        service = SolicitudService()
        data = SolicitudCreate(
            tipo_certificado="CERTIFICADO_ESTUDIO",
            comprobante_pago="REF-123"
        )
        
        response_creacion = service.crear_solicitud(usuario_id=1, data=data)
        solicitud_id = response_creacion["data"]["id"]
        
        response_cancelacion = service.cancelar_solicitud(
            solicitud_id=solicitud_id,
            usuario_id=1
        )
        
        assert response_cancelacion["success"] is True
        assert response_cancelacion["statusCode"] == 204
    
    def test_no_cancelar_solicitud_de_otro_usuario(self):
        """❌ No puedes cancelar solicitud de otro usuario"""
        service = SolicitudService()
        data = SolicitudCreate(
            tipo_certificado="CERTIFICADO_ESTUDIO",
            comprobante_pago="REF-123"
        )
        
        response_creacion = service.crear_solicitud(usuario_id=1, data=data)
        solicitud_id = response_creacion["data"]["id"]
        
        with pytest.raises(PermissionError, match="No tiene permisos"):
            service.cancelar_solicitud(
                solicitud_id=solicitud_id,
                usuario_id=2  # Otro usuario
            )
    
    def test_aprobar_solicitud_exitosamente(self):
        """✅ Admin aprueba una solicitud"""
        service = SolicitudService()
        data = SolicitudCreate(
            tipo_certificado="CERTIFICADO_ESTUDIO",
            comprobante_pago="REF-123"
        )
        
        response_creacion = service.crear_solicitud(usuario_id=1, data=data)
        solicitud_id = response_creacion["data"]["id"]
        
        datos_aprobacion = ActualizarEstadoRequest(estado="APROBADA")
        response_aprobacion = service.aprobar_rechazar_solicitud(
            solicitud_id=solicitud_id,
            data=datos_aprobacion
        )
        
        assert response_aprobacion["success"] is True
        assert response_aprobacion["data"]["estado"] == "APROBADA"
        assert response_aprobacion["message"] == "Solicitud aprobada correctamente"
    
    def test_rechazar_solicitud_exitosamente(self):
        """✅ Admin rechaza una solicitud con motivo"""
        service = SolicitudService()
        data = SolicitudCreate(
            tipo_certificado="CERTIFICADO_ESTUDIO",
            comprobante_pago="REF-123"
        )
        
        response_creacion = service.crear_solicitud(usuario_id=1, data=data)
        solicitud_id = response_creacion["data"]["id"]
        
        datos_rechazo = ActualizarEstadoRequest(
            estado="RECHAZADA",
            motivo_rechazo="Comprobante de pago no válido"
        )
        response_rechazo = service.aprobar_rechazar_solicitud(
            solicitud_id=solicitud_id,
            data=datos_rechazo
        )
        
        assert response_rechazo["success"] is True
        assert response_rechazo["data"]["estado"] == "RECHAZADA"
        assert response_rechazo["data"]["motivo_rechazo"] == "Comprobante de pago no válido"
        assert response_rechazo["message"] == "Solicitud rechazada correctamente"
    
    def test_rechazar_sin_motivo_falla(self):
        """❌ No se puede rechazar sin motivo"""
        service = SolicitudService()
        data = SolicitudCreate(
            tipo_certificado="CERTIFICADO_ESTUDIO",
            comprobante_pago="REF-123"
        )
        
        response_creacion = service.crear_solicitud(usuario_id=1, data=data)
        solicitud_id = response_creacion["data"]["id"]
        
        datos_rechazo = ActualizarEstadoRequest(estado="RECHAZADA")
        
        with pytest.raises(ValueError, match="motivo de rechazo es obligatorio"):
            service.aprobar_rechazar_solicitud(
                solicitud_id=solicitud_id,
                data=datos_rechazo
            )
    
    def test_listar_solicitudes_todas(self):
        """✅ Listar todas las solicitudes"""
        service = SolicitudService()
        
        # Crear varias solicitudes
        data1 = SolicitudCreate(tipo_certificado="CERTIFICADO_ESTUDIO", comprobante_pago="REF-001")
        data2 = SolicitudCreate(tipo_certificado="CERTIFICADO_NOTAS", comprobante_pago="REF-002")
        
        service.crear_solicitud(usuario_id=1, data=data1)
        service.crear_solicitud(usuario_id=2, data=data2)
        
        response = service.listar_solicitudes()
        
        assert response["success"] is True
        assert len(response["data"]) == 2
    
    def test_listar_solicitudes_por_estado(self):
        """✅ Listar solicitudes filtradas por estado"""
        service = SolicitudService()
        
        # Crear solicitudes
        data = SolicitudCreate(tipo_certificado="CERTIFICADO_ESTUDIO", comprobante_pago="REF-001")
        response_creacion = service.crear_solicitud(usuario_id=1, data=data)
        solicitud_id = response_creacion["data"]["id"]
        
        # Cambiar estado
        datos_aprobacion = ActualizarEstadoRequest(estado="APROBADA")
        service.aprobar_rechazar_solicitud(solicitud_id, datos_aprobacion)
        
        # Listar solo aprobadas
        response = service.listar_solicitudes(estado="APROBADA")
        
        assert response["success"] is True
        assert len(response["data"]) == 1
        assert response["data"][0]["estado"] == "APROBADA"
