# [HU-18] Anular certificado

## 📖 Historia de Usuario

**Como** administrador del sistema

**Quiero** anular un certificado emitido por error actualizando 
su estado a ANULADO

**Para** invalidar documentos incorrectos sin eliminarlos del 
sistema, manteniendo el historial y la trazabilidad de todos 
los certificados emitidos.

## 🔁 Flujo Esperado

- El administrador identifica el certificado a anular 
  desde la interfaz.
- El sistema consume el endpoint 
  `PATCH /api/v1/certificados/{id}/estado` con estado ANULADO.
- El backend valida que el certificado exista en el sistema.
- El backend valida que el certificado no esté ya anulado.
- Si las validaciones pasan, el estado del certificado 
  cambia a ANULADO.
- El PDF y el registro se conservan en el sistema para 
  auditoría pero el certificado queda inválido.
- Se retorna la información del certificado con su 
  nuevo estado.

## ✅ Criterios de Aceptación

### 1. 🔍 Estructura y lógica del servicio

- [ ] Se expone un endpoint 
      `PATCH /api/v1/certificados/{id}/estado` accesible 
      solo para rol ADMINISTRADOR.
- [ ] Se valida que el certificado con el id proporcionado 
      exista en el sistema.
- [ ] No se puede anular un certificado que ya está anulado.
- [ ] El PDF y el registro del certificado se conservan 
      en el sistema después de la anulación.
- [ ] Un certificado anulado no puede descargarse ni 
      verificarse como válido.

### 2. 📆 Estructura de la información

- [ ] La respuesta exitosa tiene la siguiente estructura:

```json
{
  "success": true,
  "statusCode": 200,
  "message": "Certificado anulado correctamente",
  "data": {
    "id": 20,
    "uuid": "550e8400-e29b-41d4-a716-446655440000",
    "estado": "ANULADO",
    "fecha_emision": "2026-03-18",
    "estudiante": {
      "nombre": "Erick Gutierrez",
      "programa_academico": "Tecnología en Sistemas"
    }
  }
}
```

- [ ] Si el certificado ya está anulado, el backend retorna:

```json
{
  "success": false,
  "statusCode": 409,
  "message": "No fue posible anular el certificado",
  "error": {
    "error_code": "CONFLICT",
    "details": "El certificado ya se encuentra anulado",
    "timestamp": "2026-03-18T10:00:00Z"
  }
}
```

- [ ] Si el certificado no existe, el backend retorna:

```json
{
  "success": false,
  "statusCode": 404,
  "message": "No fue posible anular el certificado",
  "error": {
    "error_code": "NOT_FOUND",
    "details": "No existe un certificado con el id proporcionado",
    "timestamp": "2026-03-18T10:00:00Z"
  }
}
```

## 🔧 Notas Técnicas

### 🚀 Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| `PATCH` | `/api/v1/certificados/{id}/estado` | Anula un certificado emitido por error |

### 📤 Ejemplo de Respuesta JSON

```json
{
  "success": true,
  "statusCode": 200,
  "message": "Certificado anulado correctamente",
  "data": {
    "id": 20,
    "uuid": "550e8400-e29b-41d4-a716-446655440000",
    "estado": "ANULADO",
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

### ✅ Caso 1: Anulación exitosa

- **Precondición:** El administrador está autenticado y el 
  certificado existe en estado GENERADO o DISPONIBLE.
- **Acción:** Ejecutar `PATCH /api/v1/certificados/20/estado` 
  con `estado: "ANULADO"`.
- **Resultado esperado:**
  - Código HTTP 200 OK
  - Campo `success` igual a `true`
  - Campo `estado` igual a `ANULADO`
  - El registro y PDF se conservan en el sistema

### ❌ Caso 2: Certificado ya anulado

- **Precondición:** El certificado existe pero ya está 
  en estado ANULADO.
- **Acción:** Ejecutar `PATCH /api/v1/certificados/20/estado` 
  con `estado: "ANULADO"`.
- **Resultado esperado:**
  - Código HTTP 409 Conflict
  - Campo `details` indica que el certificado ya está anulado

### ❌ Caso 3: Certificado no encontrado

- **Precondición:** No existe ningún certificado con el 
  id proporcionado.
- **Acción:** Ejecutar `PATCH /api/v1/certificados/999/estado`.
- **Resultado esperado:**
  - Código HTTP 404 Not Found
  - Campo `details` indica que el certificado no existe

### ❌ Caso 4: Acceso sin rol administrador

- **Precondición:** Un usuario con rol ESTUDIANTE intenta 
  anular un certificado.
- **Acción:** Ejecutar `PATCH /api/v1/certificados/20/estado` 
  con token de estudiante.
- **Resultado esperado:**
  - Código HTTP 403 Forbidden
  - Campo `details` indica que no tiene permisos

### ✅ Caso 5: Certificado anulado no se puede descargar

- **Precondición:** El certificado fue anulado exitosamente.
- **Acción:** Ejecutar 
  `GET /api/v1/repositorio/descarga/550e8400`.
- **Resultado esperado:**
  - Código HTTP 409 Conflict
  - Campo `details` indica que el certificado está anulado 
    y no puede descargarse

## ✅ Definición de Hecho

### 📦 Alcance Funcional

- [ ] El endpoint anula correctamente el certificado 
      actualizando su estado.
- [ ] El PDF y registro se conservan después de la anulación.
- [ ] No permite anular un certificado ya anulado.
- [ ] Un certificado anulado no puede descargarse ni 
      verificarse como válido.
- [ ] Solo el administrador puede ejecutar este endpoint.
- [ ] La respuesta JSON cumple con el contrato definido.

### 🧪 Pruebas Completadas

- [ ] Se ejecutaron pruebas para anulación exitosa y 
      certificado ya anulado.
- [ ] Se verificó que el PDF se conserva después de anular.
- [ ] Se probó que el certificado anulado no puede descargarse.
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

- [ ] Se retorna HTTP 409 cuando el certificado ya está anulado.
- [ ] Se retorna HTTP 404 cuando el certificado no existe.
- [ ] Se retorna HTTP 403 cuando el rol no tiene permiso.
- [ ] El campo `message` incluye texto claro en todos los 
      casos de error.