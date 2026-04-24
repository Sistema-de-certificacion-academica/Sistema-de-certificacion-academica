# [HU-10] Cancelar solicitud de certificado

## 📖 Historia de Usuario

**Como** estudiante del sistema

**Quiero** cancelar una solicitud de certificado que hice

**Para** retirar del proceso una solicitud que ya no necesito 
antes de que la universidad la procese.

## 🔁 Flujo Esperado

- El estudiante selecciona la solicitud que desea cancelar 
  desde la interfaz.
- El sistema consume el endpoint `DELETE /api/v1/solicitudes/{id}`.
- El backend valida que la solicitud exista y pertenezca 
  al estudiante autenticado.
- El backend valida que la solicitud esté en estado PENDIENTE.
- Si las validaciones pasan, la solicitud queda cancelada 
  del sistema.
- Se retorna confirmación de cancelación.

## ✅ Criterios de Aceptación

### 1. 🔍 Estructura y lógica del servicio

- [ ] Se expone un endpoint `DELETE /api/v1/solicitudes/{id}` 
      accesible solo para rol ESTUDIANTE.
- [ ] Se valida que la solicitud exista y pertenezca al 
      estudiante autenticado.
- [ ] Solo se puede cancelar una solicitud en estado PENDIENTE.
- [ ] No se puede cancelar una solicitud en estado APROBADA 
      o RECHAZADA.
- [ ] Un estudiante no puede cancelar solicitudes de 
      otros estudiantes.

### 2. 📆 Estructura de la información

- [ ] La respuesta exitosa retorna:

```json
{
  "success": true,
  "statusCode": 204,
  "message": "Solicitud cancelada correctamente",
  "data": null
}
```

- [ ] Si la solicitud no está en estado PENDIENTE, el backend 
      retorna:

```json
{
  "success": false,
  "statusCode": 409,
  "message": "No fue posible cancelar la solicitud",
  "error": {
    "error_code": "CONFLICT",
    "details": "Solo se pueden cancelar solicitudes en estado PENDIENTE",
    "timestamp": "2026-03-18T10:00:00Z"
  }
}
```

- [ ] Si la solicitud no existe, el backend retorna:

```json
{
  "success": false,
  "statusCode": 404,
  "message": "No fue posible cancelar la solicitud",
  "error": {
    "error_code": "NOT_FOUND",
    "details": "No existe una solicitud con el id proporcionado",
    "timestamp": "2026-03-18T10:00:00Z"
  }
}
```

## 🔧 Notas Técnicas

### 🚀 Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| `DELETE` | `/api/v1/solicitudes/{id}` | Cancela una solicitud en estado PENDIENTE |

### 📤 Ejemplo de Respuesta JSON

```json
{
  "success": true,
  "statusCode": 204,
  "message": "Solicitud cancelada correctamente",
  "data": null
}
```

## 🧪 Requisitos de Pruebas

### 🔍 Casos de Prueba Funcional

### ✅ Caso 1: Cancelación exitosa

- **Precondición:** El estudiante está autenticado, la solicitud 
  le pertenece y está en estado PENDIENTE.
- **Acción:** Ejecutar `DELETE /api/v1/solicitudes/11` con token 
  del estudiante dueño de la solicitud.
- **Resultado esperado:**
  - Código HTTP 204 No Content
  - Campo `success` igual a `true`
  - La solicitud ya no aparece en consultas posteriores

### ❌ Caso 2: Solicitud ya aprobada

- **Precondición:** La solicitud existe pero está en 
  estado APROBADA.
- **Acción:** Ejecutar `DELETE /api/v1/solicitudes/10`.
- **Resultado esperado:**
  - Código HTTP 409 Conflict
  - Campo `details` indica que solo se pueden cancelar 
    solicitudes en estado PENDIENTE

### ❌ Caso 3: Solicitud no encontrada

- **Precondición:** No existe ninguna solicitud con el 
  id proporcionado.
- **Acción:** Ejecutar `DELETE /api/v1/solicitudes/999`.
- **Resultado esperado:**
  - Código HTTP 404 Not Found
  - Campo `details` indica que la solicitud no existe

### ❌ Caso 4: Estudiante cancela solicitud ajena

- **Precondición:** La solicitud existe pero pertenece a 
  otro estudiante.
- **Acción:** Ejecutar `DELETE /api/v1/solicitudes/10` con 
  token de un estudiante diferente al dueño.
- **Resultado esperado:**
  - Código HTTP 403 Forbidden
  - Campo `details` indica que no tiene permisos para 
    cancelar esa solicitud

### ❌ Caso 5: Petición sin token

- **Precondición:** Se envía la petición sin header 
  de autorización.
- **Acción:** Ejecutar `DELETE /api/v1/solicitudes/11` sin token.
- **Resultado esperado:**
  - Código HTTP 401 Unauthorized
  - Campo `details` indica que se requiere autenticación

## ✅ Definición de Hecho

### 📦 Alcance Funcional

- [ ] El endpoint cancela correctamente solicitudes en 
      estado PENDIENTE.
- [ ] No permite cancelar solicitudes aprobadas o rechazadas.
- [ ] Un estudiante solo puede cancelar sus propias solicitudes.
- [ ] La respuesta JSON cumple con el contrato definido.

### 🧪 Pruebas Completadas

- [ ] Se ejecutaron pruebas unitarias para solicitud en estado 
      PENDIENTE, APROBADA y RECHAZADA.
- [ ] Se probó el intento de cancelar una solicitud ajena.
- [ ] Se probó la cancelación sin token.
- [ ] Las pruebas funcionales están documentadas y pasadas.

### 📄 Documentación Técnica

- [ ] Endpoint documentado en Swagger / OpenAPI.
- [ ] Se describe:
  - Propósito del endpoint
  - Campos de entrada y salida
  - Ejemplo de respuesta exitosa
  - Ejemplo de error

### 🔐 Manejo de Errores

- [ ] Se retorna HTTP 409 cuando la solicitud no está 
      en estado PENDIENTE.
- [ ] Se retorna HTTP 404 cuando la solicitud no existe.
- [ ] Se retorna HTTP 403 cuando intenta cancelar una 
      solicitud ajena.
- [ ] Se retorna HTTP 401 cuando la petición llega sin token.
- [ ] El campo `message` incluye texto claro en todos los 
      casos de error.