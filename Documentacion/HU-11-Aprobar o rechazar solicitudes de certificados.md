# [HU-11] Aprobar o rechazar solicitud de certificado

## 📖 Historia de Usuario

**Como** administrador del sistema

**Quiero** aprobar o rechazar una solicitud de certificado de un estudiante

**Para** controlar qué solicitudes proceden a la generación del certificado y cuáles no cumplen los requisitos para 
ser procesadas.

## 🔁 Flujo Esperado

- El cliente envía una petición PUT al endpoint 
  ``/api/v1/solicitudes/{id}/estado`` con el nuevo 
  estado y motivo de rechazo si aplica en el 
  cuerpo de la solicitud.
- El sistema consume el endpoint `PUT /api/v1/solicitudes/{id}/estado` 
  con el nuevo estado.
- El backend valida que la solicitud exista y esté en 
  estado PENDIENTE.
- Si se aprueba, el estado cambia a APROBADA y el sistema queda listo para iniciar la generación del certificado.
- Si se rechaza, el estado cambia a RECHAZADA con un motivo.
- Se retorna la solicitud con su estado actualizado.

## ✅ Criterios de Aceptación

### 1. 🔍 Estructura y lógica del servicio

- [ ] Se expone un endpoint `PUT /api/v1/solicitudes/{id}/estado` accesible solo para rol ADMINISTRADOR.
- [ ] Se valida que la solicitud con el id proporcionado exista en el sistema.
- [ ] Solo se puede aprobar o rechazar una solicitud en estado PENDIENTE.
- [ ] Si el campo estado contiene un valor diferente a 
      APROBADA o RECHAZADA el sistema retorna HTTP 400 
      con mensaje descriptivo.
- [ ] Si se rechaza la solicitud el campo motivo_rechazo 
      es obligatorio.
- [ ] Si se intenta modificar una solicitud ya aprobada o rechazada el sistema retorna HTTP 409 con mensaje descriptivo sin modificar ningún dato.

### 2. 📆 Estructura de la información

- [ ] La respuesta exitosa al aprobar tiene la siguiente 
      estructura:

```json
{
  "success": true,
  "statusCode": 200,
  "message": "Solicitud aprobada correctamente",
  "data": {
    "id": 10,
    "usuario_id": 1,
    "tipo_certificado": "CERTIFICADO_ESTUDIO",
    "estado": "APROBADA",
    "fecha_solicitud": "2026-03-18"
  }
}
```

- [ ] La respuesta exitosa al rechazar tiene la siguiente 
      estructura:

```json
{
  "success": true,
  "statusCode": 200,
  "message": "Solicitud rechazada correctamente",
  "data": {
    "id": 10,
    "usuario_id": 1,
    "tipo_certificado": "CERTIFICADO_ESTUDIO",
    "estado": "RECHAZADA",
    "motivo_rechazo": "Comprobante de pago no válido",
    "fecha_solicitud": "2026-03-18"
  }
}
```

- [ ] Si la solicitud no está en estado PENDIENTE, el backend 
      retorna:

```json
{
  "success": false,
  "statusCode": 409,
  "message": "No fue posible actualizar la solicitud",
  "error": {
    "error_code": "CONFLICT",
    "details": "Solo se pueden aprobar o rechazar solicitudes en estado PENDIENTE",
    "timestamp": "2026-03-18T10:00:00Z"
  }
}
```

## 🔧 Notas Técnicas

### 🚀 Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| `PUT` | `/api/v1/solicitudes/{id}/estado` | Aprueba o rechaza una solicitud pendiente |

### 📤 Ejemplo de Respuesta JSON

```json
{
  "success": true,
  "statusCode": 200,
  "message": "Solicitud aprobada correctamente",
  "data": {
    "id": 10,
    "usuario_id": 1,
    "tipo_certificado": "CERTIFICADO_ESTUDIO",
    "estado": "APROBADA",
    "fecha_solicitud": "2026-03-18"
  }
}
```

## 🧪 Requisitos de Pruebas

### 🔍 Casos de Prueba Funcional

### ✅ Caso 1: Aprobación exitosa

- **Precondición:** El administrador está autenticado y la 
  solicitud existe en estado PENDIENTE.
- **Acción:** Ejecutar `PUT /api/v1/solicitudes/10/estado` 
  con `estado: "APROBADA"`.
- **Resultado esperado:**
  - Código HTTP 200 OK
  - Campo `estado` igual a `APROBADA`
  - Campo `success` igual a `true`

### ✅ Caso 2: Rechazo exitoso

- **Precondición:** El administrador está autenticado y la 
  solicitud existe en estado PENDIENTE.
- **Acción:** Ejecutar `PUT /api/v1/solicitudes/10/estado` 
  con `estado: "RECHAZADA"` y motivo_rechazo.
- **Resultado esperado:**
  - Código HTTP 200 OK
  - Campo `estado` igual a `RECHAZADA`
  - Campo `motivo_rechazo` con el texto ingresado

### ❌ Caso 3: Solicitud no está en estado PENDIENTE

- **Precondición:** La solicitud ya fue aprobada o rechazada.
- **Acción:** Ejecutar `PUT /api/v1/solicitudes/10/estado` 
  con cualquier estado.
- **Resultado esperado:**
  - Código HTTP 409 Conflict
  - Campo `details` indica que solo se pueden gestionar 
    solicitudes en estado PENDIENTE

### ❌ Caso 4: Rechazo sin motivo

- **Precondición:** El administrador intenta rechazar una 
  solicitud sin ingresar motivo.
- **Acción:** Ejecutar `PUT /api/v1/solicitudes/10/estado` 
  con `estado: "RECHAZADA"` sin motivo_rechazo.
- **Resultado esperado:**
  - Código HTTP 400 Bad Request
  - Campo `details` indica que el motivo de rechazo 
    es obligatorio

### ❌ Caso 5: Estado no válido

- **Precondición:** El administrador envía un estado que 
  no existe en el sistema.
- **Acción:** Ejecutar `PUT /api/v1/solicitudes/10/estado` 
  con `estado: "CANCELADA"`.
- **Resultado esperado:**
  - Código HTTP 400 Bad Request
  - Campo `details` indica que el estado no es válido

### ❌ Caso 6: Acceso sin rol administrador

- **Precondición:** Un estudiante intenta aprobar una solicitud.
- **Acción:** Ejecutar `PUT /api/v1/solicitudes/10/estado` 
  con token de estudiante.
- **Resultado esperado:**
  - Código HTTP 403 Forbidden
  - Campo `details` indica que no tiene permisos

## ✅ Definición de Hecho

### 📦 Alcance Funcional

- [ ] El endpoint aprueba y rechaza correctamente solicitudes 
      en estado PENDIENTE.
- [ ] No permite gestionar solicitudes que ya fueron aprobadas 
      o rechazadas.
- [ ] El rechazo siempre requiere un motivo.
- [ ] Solo el administrador puede ejecutar este endpoint.
- [ ] La respuesta JSON cumple con el contrato definido.

### 🧪 Pruebas Completadas

- [ ] Se ejecutaron pruebas para aprobación y rechazo exitosos.
- [ ] Se probó el intento de gestionar solicitudes no pendientes.
- [ ] Se probó el rechazo sin motivo.
- [ ] Se probó el acceso con rol no autorizado.
- [ ] Las pruebas funcionales están documentadas y pasadas.

### 📄 Documentación Técnica

- [ ] Endpoint documentado en Swagger / OpenAPI.
- [ ] Se describe:
  - Propósito del endpoint
  - Campos de entrada y salida
  - Ejemplo de respuesta exitosa para aprobación
  - Ejemplo de respuesta exitosa para rechazo
  - Ejemplo de error

### 🔐 Manejo de Errores

- [ ] Se retorna HTTP 409 cuando la solicitud no está 
      en estado PENDIENTE.
- [ ] Se retorna HTTP 400 cuando el estado es inválido o 
      falta el motivo de rechazo.
- [ ] Se retorna HTTP 403 cuando el rol no tiene permiso.
- [ ] El campo `message` incluye texto claro en todos los 
      casos de error.