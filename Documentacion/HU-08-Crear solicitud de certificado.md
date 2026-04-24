# [HU-08] Crear solicitud de certificado

## 📖 Historia de Usuario

**Como** estudiante del sistema

**Quiero** crear una solicitud de certificado académico ingresando el tipo de certificado y el número de referencia de pago

**Para** iniciar el proceso de emisión del documento y que la universidad pueda revisar y aprobar mi solicitud.

## 🔁 Flujo Esperado

- El estudiante selecciona el tipo de certificado que necesita 
  desde la interfaz.
- El estudiante ingresa el número de referencia de pago.
- El sistema consume el endpoint `POST /api/v1/solicitudes` con 
  los datos de la solicitud.
- El backend valida que el estudiante no tenga una solicitud 
  pendiente del mismo tipo.
- El backend valida que el tipo de certificado sea válido.
- Si los datos son correctos, la solicitud queda creada en 
  estado PENDIENTE.
- Se retorna la información de la solicitud creada.

## ✅ Criterios de Aceptación

### 1. 🔍 Estructura y lógica del servicio

- [ ] Se expone un endpoint `POST /api/v1/solicitudes` accesible 
      solo para rol ESTUDIANTE.
- [ ] Se valida que el estudiante no tenga una solicitud del 
      mismo tipo en estado PENDIENTE.
- [ ] El tipo de certificado debe ser uno de los permitidos 
      por el sistema.
- [ ] El campo comprobante_pago es obligatorio y no puede 
      estar vacío.
- [ ] La solicitud se crea automáticamente en estado PENDIENTE.

### 2. 📆 Estructura de la información

- [ ] La respuesta exitosa tiene la siguiente estructura:

```json
{
  "success": true,
  "statusCode": 201,
  "message": "Solicitud creada correctamente",
  "data": {
    "id": 11,
    "usuario_id": 1,
    "tipo_certificado": "CERTIFICADO_ESTUDIO",
    "estado": "PENDIENTE",
    "comprobante_pago": "REF-123",
    "fecha_solicitud": "2026-03-18"
  }
}
```

- [ ] Si ya existe una solicitud pendiente del mismo tipo, 
      el backend retorna:

```json
{
  "success": false,
  "statusCode": 409,
  "message": "No fue posible crear la solicitud",
  "error": {
    "error_code": "CONFLICT",
    "details": "Ya tienes una solicitud pendiente de ese tipo de certificado",
    "timestamp": "2026-03-18T10:00:00Z"
  }
}
```

## 🔧 Notas Técnicas

### 🚀 Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| `POST` | `/api/v1/solicitudes` | Crea una nueva solicitud de certificado |

### 📤 Ejemplo de Respuesta JSON

```json
{
  "success": true,
  "statusCode": 201,
  "message": "Solicitud creada correctamente",
  "data": {
    "id": 11,
    "usuario_id": 1,
    "tipo_certificado": "CERTIFICADO_ESTUDIO",
    "estado": "PENDIENTE",
    "comprobante_pago": "REF-123",
    "fecha_solicitud": "2026-03-18"
  }
}
```

## 🧪 Requisitos de Pruebas

### 🔍 Casos de Prueba Funcional

### ✅ Caso 1: Solicitud creada exitosamente

- **Precondición:** El estudiante está autenticado y no tiene 
  una solicitud pendiente del mismo tipo.
- **Acción:** Ejecutar `POST /api/v1/solicitudes` con tipo de 
  certificado válido y referencia de pago.
- **Resultado esperado:**
  - Código HTTP 201 Created
  - Campo `success` igual a `true`
  - Campo `estado` igual a `PENDIENTE`
  - Campo `fecha_solicitud` con la fecha actual

### ❌ Caso 2: Solicitud duplicada pendiente

- **Precondición:** El estudiante ya tiene una solicitud en 
  estado PENDIENTE del mismo tipo.
- **Acción:** Ejecutar `POST /api/v1/solicitudes` con el mismo 
  tipo de certificado.
- **Resultado esperado:**
  - Código HTTP 409 Conflict
  - Campo `details` indica que ya existe una solicitud pendiente 
    de ese tipo

### ❌ Caso 3: Tipo de certificado no válido

- **Precondición:** El estudiante envía un tipo de certificado 
  que no existe en el sistema.
- **Acción:** Ejecutar `POST /api/v1/solicitudes` con 
  `tipo_certificado: "CERTIFICADO_NOTAS"`.
- **Resultado esperado:**
  - Código HTTP 400 Bad Request
  - Campo `details` indica que el tipo de certificado no es válido

### ❌ Caso 4: Comprobante de pago vacío

- **Precondición:** El estudiante envía la solicitud sin 
  referencia de pago.
- **Acción:** Ejecutar `POST /api/v1/solicitudes` sin el campo 
  comprobante_pago.
- **Resultado esperado:**
  - Código HTTP 400 Bad Request
  - Campo `details` indica que el comprobante de pago es obligatorio

### ❌ Caso 5: Acceso sin rol estudiante

- **Precondición:** Un usuario con rol ADMINISTRADOR intenta 
  crear una solicitud.
- **Acción:** Ejecutar `POST /api/v1/solicitudes` con token 
  de administrador.
- **Resultado esperado:**
  - Código HTTP 403 Forbidden
  - Campo `details` indica que no tiene permisos

## ✅ Definición de Hecho

### 📦 Alcance Funcional

- [ ] El endpoint crea correctamente la solicitud en estado PENDIENTE.
- [ ] No permite solicitudes duplicadas pendientes del mismo tipo.
- [ ] Valida que el tipo de certificado sea permitido.
- [ ] Solo el estudiante puede ejecutar este endpoint.
- [ ] La respuesta JSON cumple con el contrato definido.

### 🧪 Pruebas Completadas

- [ ] Se ejecutaron pruebas unitarias para solicitud duplicada 
      y tipo inválido.
- [ ] Se probó el envío sin comprobante de pago.
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

- [ ] Se retorna HTTP 409 cuando ya existe una solicitud 
      pendiente del mismo tipo.
- [ ] Se retorna HTTP 400 cuando el tipo de certificado es 
      inválido o el comprobante está vacío.
- [ ] Se retorna HTTP 403 cuando el rol no tiene permiso.
- [ ] El campo `message` incluye texto claro en todos los 
      casos de error.