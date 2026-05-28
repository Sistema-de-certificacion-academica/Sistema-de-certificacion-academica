# 🧪 Guía de Tests - Módulo de Solicitudes

## 📋 Contenido

Este archivo contiene **35 tests** organizados en 5 grupos principales que cubren todo el módulo de solicitudes.

### 1. **TestSolicitudCreate** (5 tests)
Valida el modelo Pydantic que recibe los datos:
- ✅ Crear solicitud con datos válidos
- ✅ Limpieza automática de espacios en comprobante
- ❌ Rechaza tipos de certificado inválidos
- ❌ Rechaza comprobante de pago vacío
- ❌ Rechaza comprobante con solo espacios

### 2. **TestSolicitudDomain** (3 tests)
Valida la lógica del modelo de dominio:
- ✅ Solicitud inicia en estado PENDIENTE
- ✅ Se puede cancelar si está PENDIENTE
- ✅ No se puede cancelar si está APROBADA

### 3. **TestSolicitudRepository** (8 tests)
Valida las operaciones de base de datos en memoria:
- ✅ Crear solicitud en repositorio
- ✅ Obtener solicitud por ID
- ✅ Retorna None si no existe
- ✅ Auto-incremento de IDs
- ✅ Obtener solicitudes por usuario
- ✅ Obtener solicitud pendiente por usuario y tipo
- ✅ Actualizar estado
- ✅ Eliminar solicitud

### 4. **TestSolicitudService** (15 tests)
Valida la lógica de negocio completa:
- ✅ Crear solicitud exitosamente
- ❌ No permite duplicados pendientes
- ✅ Consultar solicitud
- ❌ No consultar solicitud de otro usuario
- ✅ Cancelar solicitud
- ❌ No cancelar solicitud de otro
- ✅ Aprobar solicitud
- ✅ Rechazar solicitud con motivo
- ❌ Rechazar sin motivo falla
- ✅ Listar todas las solicitudes
- ✅ Listar por estado

## 🚀 Cómo Ejecutar

### Instalar pytest
```bash
pip install pytest
```

### Ejecutar todos los tests
```bash
pytest tests/test_solicitudes.py -v
```

### Ejecutar un grupo específico
```bash
pytest tests/test_solicitudes.py::TestSolicitudService -v
```

### Ejecutar un test específico
```bash
pytest tests/test_solicitudes.py::TestSolicitudService::test_crear_solicitud_exitosamente -v
```

### Ejecutar con reporte de cobertura
```bash
pip install pytest-cov
pytest tests/test_solicitudes.py --cov=app.solicitudes --cov-report=html
```

## 📊 Ejemplo de Salida Exitosa

```
tests/test_solicitudes.py::TestSolicitudCreate::test_crear_solicitud_valida PASSED                    [  2%]
tests/test_solicitudes.py::TestSolicitudCreate::test_comprobante_pago_limpia_espacios PASSED         [  5%]
tests/test_solicitudes.py::TestSolicitudCreate::test_tipo_certificado_invalido PASSED                [  8%]
tests/test_solicitudes.py::TestSolicitudCreate::test_comprobante_pago_vacio PASSED                   [ 11%]
tests/test_solicitudes.py::TestSolicitudCreate::test_comprobante_pago_solo_espacios PASSED           [ 14%]
tests/test_solicitudes.py::TestSolicitudDomain::test_solicitud_inicia_en_pendiente PASSED            [ 17%]
tests/test_solicitudes.py::TestSolicitudDomain::test_solicitud_puede_cancelarse_si_pendiente PASSED  [ 20%]
tests/test_solicitudes.py::TestSolicitudDomain::test_solicitud_no_puede_cancelarse_si_aprobada PASSED[ 23%]
tests/test_solicitudes.py::TestSolicitudRepository::test_crear_solicitud_en_repo PASSED              [ 26%]
tests/test_solicitudes.py::TestSolicitudRepository::test_obtener_solicitud_por_id PASSED             [ 29%]
tests/test_solicitudes.py::TestSolicitudRepository::test_obtener_solicitud_inexistente PASSED        [ 32%]
tests/test_solicitudes.py::TestSolicitudRepository::test_auto_incremento_ids PASSED                  [ 35%]
tests/test_solicitudes.py::TestSolicitudRepository::test_obtener_solicitudes_por_usuario PASSED      [ 38%]
tests/test_solicitudes.py::TestSolicitudRepository::test_obtener_por_usuario_y_tipo_pendiente PASSED [ 41%]
tests/test_solicitudes.py::TestSolicitudRepository::test_actualizar_estado_solicitud PASSED          [ 44%]
tests/test_solicitudes.py::TestSolicitudRepository::test_eliminar_solicitud PASSED                   [ 47%]
tests/test_solicitudes.py::TestSolicitudService::test_crear_solicitud_exitosamente PASSED            [ 50%]
tests/test_solicitudes.py::TestSolicitudService::test_no_crear_solicitud_duplicada PASSED            [ 53%]
tests/test_solicitudes.py::TestSolicitudService::test_consultar_solicitud_exitosamente PASSED        [ 56%]
tests/test_solicitudes.py::TestSolicitudService::test_consultar_solicitud_sin_permisos PASSED        [ 59%]
tests/test_solicitudes.py::TestSolicitudService::test_cancelar_solicitud_exitosamente PASSED         [ 62%]
tests/test_solicitudes.py::TestSolicitudService::test_no_cancelar_solicitud_de_otro_usuario PASSED   [ 65%]
tests/test_solicitudes.py::TestSolicitudService::test_aprobar_solicitud_exitosamente PASSED          [ 68%]
tests/test_solicitudes.py::TestSolicitudService::test_rechazar_solicitud_exitosamente PASSED         [ 71%]
tests/test_solicitudes.py::TestSolicitudService::test_rechazar_sin_motivo_falla PASSED               [ 74%]
tests/test_solicitudes.py::TestSolicitudService::test_listar_solicitudes_todas PASSED                [ 77%]
tests/test_solicitudes.py::TestSolicitudService::test_listar_solicitudes_por_estado PASSED           [ 80%]

======= 35 passed in 0.45s ======= ✅
```

## 🔍 Flujo de Test Exitoso Completo

**Escenario: Estudiante crea y luego cancela una solicitud**

```python
def test_flujo_completo_exitoso():
    """Flujo completo: crear → consultar → aprobar → listar"""
    service = SolicitudService()
    
    # 1️⃣ ESTUDIANTE crea solicitud
    data = SolicitudCreate(
        tipo_certificado="CERTIFICADO_ESTUDIO",
        comprobante_pago="TRANSF-2026-001"
    )
    response_creacion = service.crear_solicitud(usuario_id=1, data=data)
    assert response_creacion["success"] is True
    assert response_creacion["statusCode"] == 201
    solicitud_id = response_creacion["data"]["id"]
    
    # 2️⃣ ESTUDIANTE consulta su solicitud
    response_consulta = service.consultar_solicitud(
        solicitud_id=solicitud_id,
        usuario_id=1,
        rol="ESTUDIANTE"
    )
    assert response_consulta["success"] is True
    assert response_consulta["data"]["estado"] == "PENDIENTE"
    
    # 3️⃣ ADMIN aprueba la solicitud
    datos_aprobacion = ActualizarEstadoRequest(estado="APROBADA")
    response_aprobacion = service.aprobar_rechazar_solicitud(
        solicitud_id=solicitud_id,
        data=datos_aprobacion
    )
    assert response_aprobacion["success"] is True
    assert response_aprobacion["data"]["estado"] == "APROBADA"
    
    # 4️⃣ ADMIN lista solicitudes aprobadas
    response_listado = service.listar_solicitudes(estado="APROBADA")
    assert response_listado["success"] is True
    assert len(response_listado["data"]) >= 1
```

## ✨ Tips para Escribir Más Tests

### Test con contexto
```python
def test_ejemplo_descriptivo(self):
    """✅ Descripción clara de qué se prueba"""
    # Arrange - Preparar datos
    data = SolicitudCreate(...)
    
    # Act - Ejecutar la acción
    response = service.crear_solicitud(...)
    
    # Assert - Verificar el resultado
    assert response["success"] is True
```

### Usar fixtures para setup
```python
@pytest.fixture
def usuario_autenticado(self):
    return {"id": 1, "rol": "ESTUDIANTE"}

def test_con_fixture(self, usuario_autenticado):
    # usar usuario_autenticado
    pass
```

## 📝 Notas

- Todos los tests son **independientes** (limpian el repositorio antes de ejecutarse)
- Se prueban tanto **casos exitosos** (✅) como **casos de error** (❌)
- Usar `pytest -v` para ver más detalles
- Los tests usan **aserciones claras** para fácil debugging
