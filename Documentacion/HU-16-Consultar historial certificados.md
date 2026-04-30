# [HU-20] Consultar historial de certificados

## 📖 Historia de Usuario

**Como** estudiante o administrador del sistema

**Quiero** consultar el historial de certificados emitidos

**Para** revisar qué certificados han sido generados y su estado actual sin necesidad de buscarlos uno por uno.

## 🔁 Flujo Esperado

- El cliente envía una petición GET al endpoint 
 `` /api/v1/repositorio/estudiantes/{id}`` con el id 
  del estudiante como parámetro de ruta.
- El sistema consume el endpoint 
  `GET /api/v1/repositorio/estudiantes/{id}`.
- El backend valida que el usuario tenga permiso para 
  consultar ese historial.
- Se retorna la lista de certificados del estudiante con 
  su información y estado actual.

## ✅ Criterios de Aceptación

### 1. 🔍 Estructura y lógica del servicio

- [ ] Se expone un endpoint 
      `GET /api/v1/repositorio/estudiantes/{id}` accesible 
      para rol ESTUDIANTE y ADMINISTRADOR.
- [ ] Un estudiante solo puede consultar su propio historial.
- [ ] El administrador puede consultar el historial de 
      cualquier estudiante.
- [ ] Si el estudiante no tiene certificados el sistema retorna HTTP 200 con campo data como array vacío [].
- [ ] El campo estado en cada item del historial contiene únicamente uno de estos valores: GENERADO, DISPONIBLE o ANULADO sin filtrar por estado.

### 2. 📆 Estructura de la información

- [ ] La respuesta exitosa tiene la siguiente estructura:

```json
{
  "success": true,
  "statusCode": 200,
  "message": "Historial de certificados encontrado",
  "data": [
    {
      "uuid": "550e8400-e29b-41d4-a716-446655440000",
      "certificado_id": 20,
      "tipo_certificado": "CERTIFICADO_ESTUDIO",
      "fecha_emision": "2026-03-18",
      "estado": "DISPONIBLE"
    },
    {
      "uuid": "660f9500-f30c-52e5-b827-557766551111",
      "certificado_id": 21,
      "tipo_certificado": "CERTIFICADO_ESTUDIO",
      "fecha_emision": "2026-02-10",
      "estado": "ANULADO"
    }
  ]
}
```

- [ ] Si el estudiante no tiene certificados, el backend 
      retorna:

```json
{
  "success": true,
  "statusCode": 200,
  "message": "El estudiante no tiene certificados emitidos",
  "data": []
}
```

- [ ] Si el estudiante intenta consultar historial ajeno, 
      el backend retorna:

```json
{
  "success": false,
  "statusCode": 403,
  "message": "Acceso denegado",
  "error": {
    "error_code": "FORBIDDEN",
    "details": "No tiene permisos para consultar este historial",
    "timestamp": "2026-03-18T10:00:00Z"
  }
}
```

## 🔧 Notas Técnicas

### 🚀 Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/api/v1/repositorio/estudiantes/{id}` | Lista todos los certificados de un estudiante |

### 📤 Ejemplo de Respuesta JSON

```json
{
  "success": true,
  "statusCode": 200,
  "message": "Historial de certificados encontrado",
  "data": [
    {
      "uuid": "550e8400-e29b-41d4-a716-446655440000",
      "certificado_id": 20,
      "tipo_certificado": "CERTIFICADO_ESTUDIO",
      "fecha_emision": "2026-03-18",
      "estado": "DISPONIBLE"
    }
  ]
}
```

## 🧪 Requisitos de Pruebas

### 🔍 Casos de Prueba Funcional

### ✅ Caso 1: Historial exitoso con certificados

- **Precondición:** El estudiante está autenticado y tiene 
  certificados emitidos.
- **Acción:** Ejecutar 
  `GET /api/v1/repositorio/estudiantes/1` con token 
  del propio estudiante.
- **Resultado esperado:**
  - Código HTTP 200 OK
  - Campo `success` igual a `true`
  - Campo `data` contiene la lista de certificados con 
    uuid, tipo, fecha y estado

### ✅ Caso 2: Historial exitoso sin certificados

- **Precondición:** El estudiante está autenticado pero 
  no tiene certificados emitidos.
- **Acción:** Ejecutar 
  `GET /api/v1/repositorio/estudiantes/1`.
- **Resultado esperado:**
  - Código HTTP 200 OK
  - Campo `data` retorna un array vacío

### ✅ Caso 3: Administrador consulta historial de estudiante

- **Precondición:** El administrador está autenticado.
- **Acción:** Ejecutar 
  `GET /api/v1/repositorio/estudiantes/1` con token 
  de administrador.
- **Resultado esperado:**
  - Código HTTP 200 OK
  - Se retorna el historial completo del estudiante

### ❌ Caso 4: Estudiante consulta historial ajeno

- **Precondición:** El estudiante autenticado intenta consultar 
  el historial de otro estudiante.
- **Acción:** Ejecutar 
  `GET /api/v1/repositorio/estudiantes/2` con token 
  de un estudiante diferente.
- **Resultado esperado:**
  - Código HTTP 403 Forbidden
  - Campo `details` indica que no tiene permisos para 
    consultar ese historial

### ❌ Caso 5: Petición sin token

- **Precondición:** Se envía la petición sin header 
  de autorización.
- **Acción:** Ejecutar 
  `GET /api/v1/repositorio/estudiantes/1` sin token.
- **Resultado esperado:**
  - Código HTTP 401 Unauthorized
  - Campo `details` indica que se requiere autenticación

## ✅ Definición de Hecho

### 📦 Alcance Funcional

- [ ] El endpoint retorna correctamente el historial 
      de certificados del estudiante.
- [ ] Retorna lista vacía cuando el estudiante no tiene 
      certificados.
- [ ] Un estudiante solo puede consultar su propio historial.
- [ ] El administrador puede consultar el historial de 
      cualquier estudiante.
- [ ] La respuesta JSON cumple con el contrato definido.

### 🧪 Pruebas Completadas

- [ ] Se ejecutaron pruebas con historial con certificados 
      y sin certificados.
- [ ] Se probó el acceso de estudiante a historial ajeno.
- [ ] Se probó la consulta por administrador.
- [ ] Se probó la petición sin token.
- [ ] Las pruebas funcionales están documentadas y pasadas.

### 📄 Documentación Técnica

- [ ] Endpoint documentado en Swagger / OpenAPI.
- [ ] Se describe:
  - Propósito del endpoint
  - Campos de entrada y salida
  - Ejemplo de respuesta exitosa con datos
  - Ejemplo de respuesta exitosa sin datos
  - Ejemplo de error

### 🔐 Manejo de Errores

- [ ] Se retorna HTTP 403 cuando el estudiante intenta 
      consultar historial ajeno.
- [ ] Se retorna HTTP 401 cuando la petición llega sin token.
- [ ] El campo `message` incluye texto claro en todos los 
      casos de error.