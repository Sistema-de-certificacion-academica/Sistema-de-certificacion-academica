# [HU-22] Descargar certificado

## 📖 Historia de Usuario

**Como** estudiante o administrador del sistema

**Quiero** descargar el archivo PDF de un certificado usando su código UUID

**Para** obtener el documento oficial y poder usarlo o compartirlo cuando lo necesite.

## 🔁 Flujo Esperado

- El cliente envía una petición GET al endpoint 
  ``/api/v1/repositorio/descarga/{uuid}`` con el 
  UUID como parámetro de ruta.
- El sistema consume el endpoint 
  `GET /api/v1/repositorio/descarga/{uuid}`.
- El backend valida que el UUID exista en el repositorio.
- El backend valida que el certificado no esté anulado.
- El backend valida que el usuario tenga permiso para  descargar ese certificado.
- Si las validaciones pasan, el sistema retorna el 
  archivo PDF para descarga.

## ✅ Criterios de Aceptación

### 1. 🔍 Estructura y lógica del servicio

- [ ] Se expone un endpoint 
      `GET /api/v1/repositorio/descarga/{uuid}` accesible 
      para rol ESTUDIANTE y ADMINISTRADOR.
- [ ] Se valida que el UUID exista en el repositorio.
- [ ] Si el certificado tiene estado ANULADO el sistema retorna HTTP 409 con mensaje descriptivo sin 
      retornar ningún archivo.
- [ ] Un estudiante solo puede descargar sus propios 
      certificados.
- [ ] El administrador puede descargar cualquier certificado.
- [ ] El sistema retorna el archivo PDF almacenado en la ruta registrada en el repositorio para ese UUID,   con header Content-Type: application/pdf y     Content-Disposition: attachment.

### 2. 📆 Estructura de la información

- [ ] La respuesta exitosa retorna el archivo PDF directamente para descarga con los headers correctos:
```
HTTP/1.1 200 OK
Content-Type: application/pdf
Content-Disposition: attachment; filename="certificado_550e8400.pdf"
```


- [ ] Si el certificado está anulado, el backend retorna:

```json
{
  "success": false,
  "statusCode": 409,
  "message": "No fue posible descargar el certificado",
  "error": {
    "error_code": "CONFLICT",
    "details": "El certificado está anulado y no puede descargarse",
    "timestamp": "2026-03-18T10:00:00Z"
  }
}
```

- [ ] Si el UUID no existe, el backend retorna:

```json
{
  "success": false,
  "statusCode": 404,
  "message": "No fue posible descargar el certificado",
  "error": {
    "error_code": "NOT_FOUND",
    "details": "No existe un certificado con el UUID proporcionado",
    "timestamp": "2026-03-18T10:00:00Z"
  }
}
```

## 🔧 Notas Técnicas

### 🚀 Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/api/v1/repositorio/descarga/{uuid}` | Descarga el PDF de un certificado por UUID |

### 📤 Ejemplo de Respuesta

La respuesta exitosa no retorna JSON sino el archivo PDF 
directamente con los siguientes headers:

```
HTTP/1.1 200 OK
Content-Type: application/pdf
Content-Disposition: attachment; filename="certificado_550e8400.pdf"
```

Los errores sí retornan el formato JSON estándar del sistema.

## 🧪 Requisitos de Pruebas

### 🔍 Casos de Prueba Funcional

### ✅ Caso 1: Descarga exitosa por estudiante

- **Precondición:** El estudiante está autenticado, el UUID 
  existe y el certificado le pertenece y está disponible.
- **Acción:** Ejecutar 
  `GET /api/v1/repositorio/descarga/550e8400` con token 
  del estudiante dueño del certificado.
- **Resultado esperado:**
  - Código HTTP 200 OK
  - Respuesta es el archivo PDF
  - Header `Content-Disposition` con nombre del archivo

### ✅ Caso 2: Descarga exitosa por administrador

- **Precondición:** El administrador está autenticado y el 
  UUID existe en el repositorio.
- **Acción:** Ejecutar 
  `GET /api/v1/repositorio/descarga/550e8400` con token 
  de administrador.
- **Resultado esperado:**
  - Código HTTP 200 OK
  - Respuesta es el archivo PDF del certificado

### ❌ Caso 3: Certificado anulado

- **Precondición:** El certificado existe pero su estado 
  es ANULADO.
- **Acción:** Ejecutar 
  `GET /api/v1/repositorio/descarga/550e8400`.
- **Resultado esperado:**
  - Código HTTP 409 Conflict
  - Campo `details` indica que el certificado está anulado 
    y no puede descargarse

### ❌ Caso 4: UUID no encontrado

- **Precondición:** No existe ningún certificado con el 
  UUID proporcionado.
- **Acción:** Ejecutar 
  `GET /api/v1/repositorio/descarga/uuid-inexistente`.
- **Resultado esperado:**
  - Código HTTP 404 Not Found
  - Campo `details` indica que el certificado no existe

### ❌ Caso 5: Estudiante descarga certificado ajeno

- **Precondición:** El UUID existe pero pertenece a otro 
  estudiante.
- **Acción:** Ejecutar 
  `GET /api/v1/repositorio/descarga/550e8400` con token 
  de un estudiante diferente al dueño.
- **Resultado esperado:**
  - Código HTTP 403 Forbidden
  - Campo `details` indica que no tiene permisos para 
    descargar ese certificado

### ❌ Caso 6: Petición sin token

- **Precondición:** Se envía la petición sin header 
  de autorización.
- **Acción:** Ejecutar 
  `GET /api/v1/repositorio/descarga/550e8400` sin token.
- **Resultado esperado:**
  - Código HTTP 401 Unauthorized
  - Campo `details` indica que se requiere autenticación

## ✅ Definición de Hecho

### 📦 Alcance Funcional

- [ ] El endpoint retorna correctamente el archivo PDF 
      para descarga.
- [ ] No permite descargar certificados anulados.
- [ ] Un estudiante solo puede descargar sus propios 
      certificados.
- [ ] El administrador puede descargar cualquier certificado.
- [ ] La respuesta incluye los headers correctos para 
      descarga de PDF.

### 🧪 Pruebas Completadas

- [ ] Se ejecutaron pruebas para descarga exitosa por 
      estudiante y administrador.
- [ ] Se probó la descarga de certificado anulado.
- [ ] Se probó con UUID inexistente.
- [ ] Se probó el acceso de estudiante a certificado ajeno.
- [ ] Se probó la descarga sin token.
- [ ] Las pruebas funcionales están documentadas y pasadas.

### 📄 Documentación Técnica

- [ ] Endpoint documentado en Swagger / OpenAPI.
- [ ] Se describe:
  - Propósito del endpoint
  - Campos de entrada
  - Headers de respuesta exitosa
  - Ejemplo de error

### 🔐 Manejo de Errores

- [ ] Se retorna HTTP 409 cuando el certificado está anulado.
- [ ] Se retorna HTTP 404 cuando el UUID no existe.
- [ ] Se retorna HTTP 403 cuando el estudiante intenta 
      descargar un certificado ajeno.
- [ ] Se retorna HTTP 401 cuando la petición llega sin token.
- [ ] El campo `message` incluye texto claro en todos los 
      casos de error.