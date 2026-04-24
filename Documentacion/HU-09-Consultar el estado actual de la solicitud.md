# [HU-09] Consultar el estado actual de la solicitud

## 📖 Historia de Usuario

**Como** estudiante del sistema

**Quiero** consultar el estado actual de una solicitud de certificado que hice

**Para** saber si mi solicitud está pendiente, fue aprobada o rechazada por la universidad sin necesidad de contactarla 
directamente.

## 🔁 Flujo Esperado

- El estudiante selecciona la solicitud que quiere consultar 
  desde la interfaz.
- El sistema consume el endpoint `GET /api/v1/solicitudes/{id}` 
  con el id de la solicitud.
- El backend valida que la solicitud exista y pertenezca 
  al estudiante autenticado.
- Se retorna la información de la solicitud con su estado actual.

## ✅ Criterios de Aceptación

### 1. 🔍 Estructura y lógica del servicio

- [ ] Se expone un endpoint `GET /api/v1/solicitudes/{id}` 
      accesible para rol ESTUDIANTE y ADMINISTRADOR.
- [ ] Se valida que la solicitud con el id proporcionado 
      exista en el sistema.
- [ ] Un estudiante solo puede consultar sus propias solicitudes, 
      no las de otros estudiantes.
- [ ] El administrador puede consultar cualquier solicitud.
- [ ] El estado retornado puede ser PENDIENTE, APROBADA 
      o RECHAZADA.

### 2. 📆 Estructura de la información

- [ ] La respuesta exitosa tiene la siguiente estructura:

```json
{
  "success": true,
  "statusCode": 200,
  "message": "Solicitud encontrada",
  "data": {
    "id": 10,
    "usuario_id": 1,
    "tipo_certificado": "CERTIFICADO_ESTUDIO",
    "estado": "APROBADA",
    "comprobante_pago": "REF-123",
    "fecha_solicitud": "2026-03-18"
  }
}
```

- [ ] Si la solicitud no existe, el backend retorna:

```json
{
  "success": false,
  "statusCode": 404,
  "message": "No fue posible consultar la solicitud",
  "error": {
    "error_code": "NOT_FOUND",
    "details": "No existe una solicitud con el id proporcionado",
    "timestamp": "2026-03-18T10:00:00Z"
  }
}
```

- [ ] Si el estudiante intenta consultar una solicitud de otro estudiante, el backend retorna:

```json
{
  "success": false,
  "statusCode": 403,
  "message": "Acceso denegado",
  "error": {
    "error_code": "FORBIDDEN",
    "details": "No tiene permisos para consultar esta solicitud",
    "timestamp": "2026-03-18T10:00:00Z"
  }
}
```

## 🔧 Notas Técnicas

### 🚀 Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/api/v1/solicitudes/{id}` | Consulta el estado actual de una solicitud |

### 📤 Ejemplo de Respuesta JSON

```json
{
  "success": true,
  "statusCode": 200,
  "message": "Solicitud encontrada",
  "data": {
    "id": 10,
    "usuario_id": 1,
    "tipo_certificado": "CERTIFICADO_ESTUDIO",
    "estado": "APROBADA",
    "comprobante_pago": "REF-123",
    "fecha_solicitud": "2026-03-18"
  }
}
```

## 🧪 Requisitos de Pruebas

### 🔍 Casos de Prueba Funcional

### ✅ Caso 1: Consulta exitosa por estudiante

- **Precondición:** El estudiante está autenticado y la solicitud 
  le pertenece.
- **Acción:** Ejecutar `GET /api/v1/solicitudes/10` con token 
  del estudiante dueño de la solicitud.
- **Resultado esperado:**
  - Código HTTP 200 OK
  - Campo `success` igual a `true`
  - Campo `estado` con el valor actual de la solicitud

### ✅ Caso 2: Consulta exitosa por administrador

- **Precondición:** El administrador está autenticado.
- **Acción:** Ejecutar `GET /api/v1/solicitudes/10` con token 
  de administrador.
- **Resultado esperado:**
  - Código HTTP 200 OK
  - Se retorna la información completa de la solicitud

### ❌ Caso 3: Solicitud no encontrada

- **Precondición:** No existe ninguna solicitud con el id 
  proporcionado.
- **Acción:** Ejecutar `GET /api/v1/solicitudes/999`.
- **Resultado esperado:**
  - Código HTTP 404 Not Found
  - Campo `details` indica que la solicitud no existe

### ❌ Caso 4: Estudiante consulta solicitud de otro estudiante

- **Precondición:** La solicitud existe pero pertenece a 
  otro estudiante.
- **Acción:** Ejecutar `GET /api/v1/solicitudes/10` con token 
  de un estudiante diferente al dueño.
- **Resultado esperado:**
  - Código HTTP 403 Forbidden
  - Campo `details` indica que no tiene permisos para 
    consultar esa solicitud

### ❌ Caso 5: Petición sin token

- **Precondición:** Se envía la petición sin header 
  de autorización.
- **Acción:** Ejecutar `GET /api/v1/solicitudes/10` sin token.
- **Resultado esperado:**
  - Código HTTP 401 Unauthorized
  - Campo `details` indica que se requiere autenticación

## ✅ Definición de Hecho

### 📦 Alcance Funcional

- [ ] El endpoint retorna correctamente el estado de la solicitud.
- [ ] Un estudiante solo puede ver sus propias solicitudes.
- [ ] El administrador puede consultar cualquier solicitud.
- [ ] La respuesta JSON cumple con el contrato definido.

### 🧪 Pruebas Completadas

- [ ] Se ejecutaron pruebas unitarias para solicitud existente 
      e inexistente.
- [ ] Se probó el acceso de un estudiante a solicitud ajena.
- [ ] Se probó la consulta sin token.
- [ ] Las pruebas funcionales están documentadas y pasadas.

### 📄 Documentación Técnica

- [ ] Endpoint documentado en Swagger / OpenAPI.
- [ ] Se describe:
  - Propósito del endpoint
  - Campos de entrada y salida
  - Ejemplo de respuesta exitosa
  - Ejemplo de error

### 🔐 Manejo de Errores

- [ ] Se retorna HTTP 404 cuando la solicitud no existe.
- [ ] Se retorna HTTP 403 cuando el estudiante intenta consultar 
      una solicitud ajena.
- [ ] Se retorna HTTP 401 cuando la petición llega sin token.
- [ ] El campo `message` incluye texto claro en todos los 
      casos de error.