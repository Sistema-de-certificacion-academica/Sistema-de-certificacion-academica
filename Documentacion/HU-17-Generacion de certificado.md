# [HU-17] Generar certificado digital

## 📖 Historia de Usuario

**Como** administrador del sistema

**Quiero** generar el certificado digital de un estudiante seleccionando su solicitud aprobada y una plantilla activa

**Para** producir un documento PDF oficial con los datos del 
estudiante, un código UUID único y firma digital que garantice su autenticidad.

## 🔁 Flujo Esperado

- El cliente envía una petición POST al endpoint 
  ``/api/v1/certificados`` con el id de la solicitud 
  aprobada y el id de la plantilla en el cuerpo 
  de la solicitud.
- El sistema consume el endpoint `POST /api/v1/certificados` 
  con el id de la solicitud y el id de la plantilla.
- El backend valida que la solicitud exista y esté en 
  estado APROBADA.
- El backend valida que la plantilla exista y esté activa.
- El sistema combina los datos del estudiante con los campos 
  dinámicos de la plantilla.
- Se genera un UUID único para el certificado.
- Se genera el documento en formato PDF usando ReportLab.
- Se asigna la firma digital al certificado.
- El certificado queda registrado en el sistema con estado 
- El sistema almacena automáticamente el certificado generado en el repositorio con sus metadatos y ruta del PDF
  GENERADO.
- Se retorna la información del certificado creado.

## ✅ Criterios de Aceptación

### 1. 🔍 Estructura y lógica del servicio

- [ ] Se expone un endpoint `POST /api/v1/certificados` accesible 
      solo para rol ADMINISTRADOR.
- [ ] Se valida que la solicitud exista y esté en estado APROBADA.
- [ ] Se valida que la plantilla exista y esté activa.
- [ ] El UUID se genera con el estándar UUID4 y el sistema verifica que no exista en la base de datos antes  de asignarlo. Si existiera genera uno nuevo 
      automáticamente.
- [ ] El PDF generado incluye los campos dinámicos de la plantilla completados con los datos del estudiante.
- [ ] El campo estado en la respuesta retorna GENERADO 
      y el certificado queda almacenado automáticamente en el repositorio con su uuid, ruta del PDF 
      y fecha de emisión.
- [ ] El certificado generado queda automáticamente almacenado en el repositorio con su uuid, ruta del archivo PDF y fecha de emisión.

### 2. 📆 Estructura de la información

- [ ] La respuesta exitosa tiene la siguiente estructura:

```json
{
  "success": true,
  "statusCode": 201,
  "message": "Certificado generado correctamente",
  "data": {
    "id": 20,
    "uuid": "550e8400-e29b-41d4-a716-446655440000",
    "solicitud_id": 10,
    "plantilla_id": 5,
    "estado": "GENERADO",
    "fecha_emision": "2026-03-18",
    "estudiante": {
      "nombre": "Erick Gutierrez",
      "programa_academico": "Tecnología en Sistemas"
    }
  }
}
```

- [ ] Si la solicitud no está aprobada, el backend retorna:

```json
{
  "success": false,
  "statusCode": 409,
  "message": "No fue posible generar el certificado",
  "error": {
    "error_code": "CONFLICT",
    "details": "Solo se pueden generar certificados de solicitudes aprobadas",
    "timestamp": "2026-03-18T10:00:00Z"
  }
}
```

- [ ] Si la plantilla no está activa, el backend retorna:

```json
{
  "success": false,
  "statusCode": 409,
  "message": "No fue posible generar el certificado",
  "error": {
    "error_code": "CONFLICT",
    "details": "La plantilla seleccionada no está activa",
    "timestamp": "2026-03-18T10:00:00Z"
  }
}
```

## 🔧 Notas Técnicas

### 🚀 Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| `POST` | `/api/v1/certificados` | Genera el certificado digital del estudiante |
| `GET` | `/api/v1/certificados/{id}` | Consulta la información de un certificado generado |

### 📤 Ejemplo de Respuesta JSON

```json
{
  "success": true,
  "statusCode": 201,
  "message": "Certificado generado correctamente",
  "data": {
    "id": 20,
    "uuid": "550e8400-e29b-41d4-a716-446655440000",
    "solicitud_id": 10,
    "plantilla_id": 5,
    "estado": "GENERADO",
    "fecha_emision": "2026-03-18",
    "estudiante": {
      "nombre": "Erick Gutierrez",
      "programa_academico": "Tecnología en Sistemas"
    }
  }
}
```

## 🧪 Requisitos de Pruebas

### 🔍 Casos de Prueba Funcional

### ✅ Caso 1: Generación exitosa

- **Precondición:** El administrador está autenticado, la solicitud 
  está en estado APROBADA y la plantilla está activa.
- **Acción:** Ejecutar `POST /api/v1/certificados` con 
  solicitud_id y plantilla_id válidos.
- **Resultado esperado:**
  - Código HTTP 201 Created
  - Campo `success` igual a `true`
  - Campo `uuid` presente y único
  - Campo `estado` igual a `GENERADO`
  - PDF generado correctamente con los datos del estudiante

### ❌ Caso 2: Solicitud no aprobada

- **Precondición:** La solicitud existe pero está en 
  estado PENDIENTE o RECHAZADA.
- **Acción:** Ejecutar `POST /api/v1/certificados` con 
  esa solicitud_id.
- **Resultado esperado:**
  - Código HTTP 409 Conflict
  - Campo `details` indica que la solicitud no está aprobada

### ❌ Caso 3: Plantilla no activa

- **Precondición:** La plantilla existe pero está inactiva 
  en el sistema.
- **Acción:** Ejecutar `POST /api/v1/certificados` con 
  esa plantilla_id.
- **Resultado esperado:**
  - Código HTTP 409 Conflict
  - Campo `details` indica que la plantilla no está activa

### ❌ Caso 4: Solicitud no encontrada

- **Precondición:** No existe ninguna solicitud con el 
  id proporcionado.
- **Acción:** Ejecutar `POST /api/v1/certificados` con 
  solicitud_id inexistente.
- **Resultado esperado:**
  - Código HTTP 404 Not Found
  - Campo `details` indica que la solicitud no existe

### ❌ Caso 5: Acceso sin rol administrador

- **Precondición:** Un usuario con rol ESTUDIANTE intenta 
  generar un certificado.
- **Acción:** Ejecutar `POST /api/v1/certificados` con 
  token de estudiante.
- **Resultado esperado:**
  - Código HTTP 403 Forbidden
  - Campo `details` indica que no tiene permisos

## ✅ Definición de Hecho

### 📦 Alcance Funcional

- [ ] El endpoint genera correctamente el certificado en 
      formato PDF.
- [ ] El UUID asignado es único en todo el sistema.
- [ ] Solo se generan certificados de solicitudes aprobadas.
- [ ] Solo se usan plantillas activas para la generación.
- [ ] Solo el administrador puede ejecutar este endpoint.
- [ ] La respuesta JSON cumple con el contrato definido.
- [ ] El certificado queda almacenado en el repositorio automáticamente sin intervención del administrador

### 🧪 Pruebas Completadas

- [ ] Se ejecutaron pruebas para generación exitosa y 
      solicitud no aprobada.
- [ ] Se probó con plantilla inactiva y solicitud inexistente.
- [ ] Se probó el acceso con rol no autorizado.
- [ ] Las pruebas funcionales están documentadas y pasadas.

### 📄 Documentación Técnica

- [ ] Endpoint documentado en Swagger / OpenAPI.
- [ ] Se describe:
  - Propósito del endpoint
  - Campos de entrada y salida
  - Ejemplo de respuesta exitosa
  - Ejemplo de error

### 🔐 Manejo de Errores

- [ ] Se retorna HTTP 409 cuando la solicitud no está aprobada 
      o la plantilla no está activa.
- [ ] Se retorna HTTP 404 cuando la solicitud o plantilla 
      no existen.
- [ ] Se retorna HTTP 403 cuando el rol no tiene permiso.
- [ ] El campo `message` incluye texto claro en todos los 
      casos de error.