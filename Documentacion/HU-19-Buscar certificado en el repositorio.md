# [HU-19] Buscar certificado en el repositorio

## 📖 Historia de Usuario

**Como** estudiante o administrador del sistema

**Quiero** buscar un certificado en el repositorio usando su código UUID

**Para** acceder a la información y estado del certificado de forma rápida sin necesidad de navegar por todo el historial

## 🔁 Flujo Esperado

- El cliente envía una petición GET al endpoint 
  ``/api/v1/repositorio/certificados/{uuid}`` con el 
  UUID como parámetro de ruta.
- El sistema consume el endpoint 
  `GET /api/v1/repositorio/certificados/{uuid}`.
- El backend busca el certificado en el repositorio   usando el UUID proporcionado.
- Si existe, retorna la información completa del certificado   con su estado actual.

## ✅ Criterios de Aceptación

### 1. 🔍 Estructura y lógica del servicio

- [ ] Se expone un endpoint 
      `GET /api/v1/repositorio/certificados/{uuid}` accesible 
      para rol ESTUDIANTE y ADMINISTRADOR.
- [ ] Se valida que el UUID proporcionado exista en el repositorio.
- [ ] Si el uuid del certificado no pertenece al estudiante autenticado el sistema retorna HTTP 403 con mensaje descriptivo sin retornar ningún dato del certificado.
- [ ] El administrador puede buscar cualquier certificado.
- [ ] El campo estado en la respuesta contiene únicamente uno de estos valores: DISPONIBLE o ANULADO. 
      Cualquier otro valor es un error del sistema.

### 2. 📆 Estructura de la información

- [ ] La respuesta exitosa tiene la siguiente estructura:

```json
{
  "success": true,
  "statusCode": 200,
  "message": "Certificado encontrado",
  "data": {
    "uuid": "550e8400",
    "certificado_id": 20,
    "fecha_emision": "2026-03-18",
    "estado": "DISPONIBLE",
    "ruta_archivo": "/certificados/certificado_20.pdf"
  }
}
```

- [ ] Si el UUID no existe en el repositorio, el backend 
      retorna:

```json
{
  "success": false,
  "statusCode": 404,
  "message": "No fue posible encontrar el certificado",
  "error": {
    "error_code": "NOT_FOUND",
    "details": "No existe un certificado con el UUID proporcionado",
    "timestamp": "2026-03-18T10:00:00Z"
  }
}
```

- [ ] Si el estudiante intenta buscar un certificado ajeno, 
      el backend retorna:

```json
{
  "success": false,
  "statusCode": 403,
  "message": "Acceso denegado",
  "error": {
    "error_code": "FORBIDDEN",
    "details": "No tiene permisos para consultar este certificado",
    "timestamp": "2026-03-18T10:00:00Z"
  }
}
```

## 🔧 Notas Técnicas

### 🚀 Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/api/v1/repositorio/certificados/{uuid}` | Busca un certificado por su UUID |

### 📤 Ejemplo de Respuesta JSON

```json
{
  "success": true,
  "statusCode": 200,
  "message": "Certificado encontrado",
  "data": {
    "uuid": "550e8400",
    "certificado_id": 20,
    "fecha_emision": "2026-03-18",
    "estado": "DISPONIBLE",
    "ruta_archivo": "/certificados/certificado_20.pdf"
  }
}
```

## 🧪 Requisitos de Pruebas

### 🔍 Casos de Prueba Funcional

### ✅ Caso 1: Búsqueda exitosa por estudiante

- **Precondición:** El estudiante está autenticado y el UUID 
  corresponde a uno de sus certificados.
- **Acción:** Ejecutar 
  `GET /api/v1/repositorio/certificados/550e8400` con token 
  del estudiante dueño del certificado.
- **Resultado esperado:**
  - Código HTTP 200 OK
  - Campo `success` igual a `true`
  - Campo `estado` con el valor actual del certificado

### ✅ Caso 2: Búsqueda exitosa por administrador

- **Precondición:** El administrador está autenticado y el 
  UUID existe en el repositorio.
- **Acción:** Ejecutar 
  `GET /api/v1/repositorio/certificados/550e8400` con token 
  de administrador.
- **Resultado esperado:**
  - Código HTTP 200 OK
  - Se retorna la información completa del certificado

### ❌ Caso 3: UUID no encontrado

- **Precondición:** No existe ningún certificado con el 
  UUID proporcionado.
- **Acción:** Ejecutar 
  `GET /api/v1/repositorio/certificados/uuid-inexistente`.
- **Resultado esperado:**
  - Código HTTP 404 Not Found
  - Campo `details` indica que el certificado no existe

### ❌ Caso 4: Estudiante busca certificado ajeno

- **Precondición:** El UUID existe pero pertenece a otro 
  estudiante.
- **Acción:** Ejecutar 
  `GET /api/v1/repositorio/certificados/550e8400` con token 
  de un estudiante diferente al dueño.
- **Resultado esperado:**
  - Código HTTP 403 Forbidden
  - Campo `details` indica que no tiene permisos para 
    consultar ese certificado

### ❌ Caso 5: Petición sin token

- **Precondición:** Se envía la petición sin header 
  de autorización.
- **Acción:** Ejecutar 
  `GET /api/v1/repositorio/certificados/550e8400` sin token.
- **Resultado esperado:**
  - Código HTTP 401 Unauthorized
  - Campo `details` indica que se requiere autenticación

## ✅ Definición de Hecho

### 📦 Alcance Funcional

- [ ] El endpoint retorna correctamente la información del 
      certificado por UUID.
- [ ] Un estudiante solo puede buscar sus propios certificados.
- [ ] El administrador puede buscar cualquier certificado.
- [ ] La respuesta JSON cumple con el contrato definido.

### 🧪 Pruebas Completadas

- [ ] Se ejecutaron pruebas para UUID existente e inexistente.
- [ ] Se probó el acceso de un estudiante a certificado ajeno.
- [ ] Se probó la búsqueda sin token.
- [ ] Las pruebas funcionales están documentadas y pasadas.

### 📄 Documentación Técnica

- [ ] Endpoint documentado en Swagger / OpenAPI.
- [ ] Se describe:
  - Propósito del endpoint
  - Campos de entrada y salida
  - Ejemplo de respuesta exitosa
  - Ejemplo de error

### 🔐 Manejo de Errores

- [ ] Se retorna HTTP 404 cuando el UUID no existe.
- [ ] Se retorna HTTP 403 cuando el estudiante busca 
      un certificado ajeno.
- [ ] Se retorna HTTP 401 cuando la petición llega sin token.
- [ ] El campo `message` incluye texto claro en todos los 
      casos de error.