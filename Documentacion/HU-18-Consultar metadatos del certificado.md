# [HU-21] Consultar metadatos del certificado

## 📖 Historia de Usuario

**Como** empresa o persona externa

**Quiero** consultar los metadatos básicos de un certificado 
usando su código UUID sin necesidad de autenticarme

**Para** verificar rápidamente la fecha de emisión, vigencia 
y estado del documento sin necesidad de descargarlo completo.

## 🔁 Flujo Esperado

- El cliente envía una petición GET al endpoint 
  ``/api/v1/repositorio/metadatos/{uuid}`` con el 
  UUID como parámetro de ruta.
- El sistema consume el endpoint 
  `GET /api/v1/repositorio/metadatos/{uuid}`.
- El backend busca el certificado en el repositorio 
  usando el UUID proporcionado.
- Si existe, retorna los metadatos básicos del certificado 
  sin exponer información privada del estudiante.

## ✅ Criterios de Aceptación

### 1. 🔍 Estructura y lógica del servicio

- [ ] Se expone un endpoint 
      `GET /api/v1/repositorio/metadatos/{uuid}` de acceso 
      público, no requiere autenticación.
- [ ] Se valida que el UUID proporcionado exista en 
      el repositorio.
- [ ] La respuesta incluye únicamente los campos uuid, 
      tipo_certificado, fecha_emision y estado. Ningún 
      dato personal del estudiante como nombre, correo 
      o id es retornado en este endpoint.
- [ ] No se expone información privada del estudiante 
      como correo o datos personales sensibles.
- [ ] Un certificado anulado retorna estado ANULADO 
      en los metadatos.

### 2. 📆 Estructura de la información

- [ ] La respuesta exitosa tiene la siguiente estructura:

```json
{
  "success": true,
  "statusCode": 200,
  "message": "Metadatos del certificado encontrados",
  "data": {
    "uuid": "550e8400-e29b-41d4-a716-446655440000",
    "tipo_certificado": "CERTIFICADO_ESTUDIO",
    "fecha_emision": "2026-03-18",
    "estado": "DISPONIBLE"
  }
}
```

- [ ] Si el UUID no existe, el backend retorna:

```json
{
  "success": false,
  "statusCode": 404,
  "message": "No fue posible consultar los metadatos",
  "error": {
    "error_code": "NOT_FOUND",
    "details": "No existe un certificado con el UUID proporcionado",
    "timestamp": "2026-03-18T10:00:00Z"
  }
}
```

- [ ] Si el UUID tiene formato inválido, el backend retorna:

```json
{
  "success": false,
  "statusCode": 400,
  "message": "No fue posible consultar los metadatos",
  "error": {
    "error_code": "BAD_REQUEST",
    "details": "El formato del UUID no es válido",
    "timestamp": "2026-03-18T10:00:00Z"
  }
}
```

## 🔧 Notas Técnicas

### 🚀 Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/api/v1/repositorio/metadatos/{uuid}` | Consulta metadatos básicos de un certificado |

### 📤 Ejemplo de Respuesta JSON

```json
{
  "success": true,
  "statusCode": 200,
  "message": "Metadatos del certificado encontrados",
  "data": {
    "uuid": "550e8400-e29b-41d4-a716-446655440000",
    "tipo_certificado": "CERTIFICADO_ESTUDIO",
    "fecha_emision": "2026-03-18",
    "estado": "DISPONIBLE"
  }
}
```

## 🧪 Requisitos de Pruebas

### 🔍 Casos de Prueba Funcional

### ✅ Caso 1: Consulta exitosa de metadatos

- **Precondición:** El UUID existe en el repositorio.
- **Acción:** Ejecutar 
  `GET /api/v1/repositorio/metadatos/550e8400` sin token.
- **Resultado esperado:**
  - Código HTTP 200 OK
  - Campo `success` igual a `true`
  - Campo `data` contiene uuid, tipo, fecha y estado
  - No se expone información privada del estudiante

### ✅ Caso 2: Metadatos de certificado anulado

- **Precondición:** El UUID existe pero el certificado 
  está anulado.
- **Acción:** Ejecutar 
  `GET /api/v1/repositorio/metadatos/550e8400`.
- **Resultado esperado:**
  - Código HTTP 200 OK
  - Campo `estado` igual a `ANULADO`

### ❌ Caso 3: UUID no encontrado

- **Precondición:** No existe ningún certificado con el 
  UUID proporcionado.
- **Acción:** Ejecutar 
  `GET /api/v1/repositorio/metadatos/uuid-inexistente`.
- **Resultado esperado:**
  - Código HTTP 404 Not Found
  - Campo `details` indica que el certificado no existe

### ❌ Caso 4: UUID con formato inválido

- **Precondición:** El usuario ingresa un UUID con 
  formato incorrecto.
- **Acción:** Ejecutar 
  `GET /api/v1/repositorio/metadatos/123`.
- **Resultado esperado:**
  - Código HTTP 400 Bad Request
  - Campo `details` indica que el formato del UUID 
    no es válido

## ✅ Definición de Hecho

### 📦 Alcance Funcional

- [ ] El endpoint retorna correctamente los metadatos 
      del certificado.
- [ ] El acceso es público, no requiere autenticación.
- [ ] No expone información privada del estudiante.
- [ ] Retorna estado ANULADO para certificados anulados.
- [ ] La respuesta JSON cumple con el contrato definido.

### 🧪 Pruebas Completadas

- [ ] Se ejecutaron pruebas para UUID existente, anulado 
      e inexistente.
- [ ] Se verificó que no se expone información privada.
- [ ] Se probó con UUID de formato inválido.
- [ ] Las pruebas funcionales están documentadas y pasadas.

### 📄 Documentación Técnica

- [ ] Endpoint documentado en Swagger / OpenAPI.
- [ ] Se describe:
  - Propósito del endpoint
  - Campos de salida
  - Ejemplo de respuesta exitosa
  - Ejemplo de error

### 🔐 Manejo de Errores

- [ ] Se retorna HTTP 404 cuando el UUID no existe.
- [ ] Se retorna HTTP 400 cuando el UUID tiene formato inválido.
- [ ] El campo `message` incluye texto claro en todos los 
      casos de error.