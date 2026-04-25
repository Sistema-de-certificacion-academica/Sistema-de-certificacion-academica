# [HU-24] Validar integridad del certificado

## 📖 Historia de Usuario

**Como** empresa o persona externa

**Quiero** validar que el archivo de un certificado no ha sido modificado desde su emisión usando su código UUID

**Para** asegurarme de que el documento que recibí es exactamente el mismo que emitió la universidad y no ha sido alterado.

## 🔁 Flujo Esperado

- El verificador ingresa el UUID del certificado en la interfaz pública de verificación de integridad.
- El sistema consume el endpoint 
  `GET /api/v1/verificaciones/integridad/{uuid}`.
- El backend busca el certificado en el repositorio usando el UUID proporcionado.
- El sistema recalcula el hash SHA-256 del archivo PDF actual y lo compara con el hash guardado al momento 
  de la emisión.
- Si los hashes coinciden el documento es íntegro.
- Si no coinciden el documento fue alterado.
- Se retorna el resultado de la validación.

## ✅ Criterios de Aceptación

### 1. 🔍 Estructura y lógica del servicio

- [ ] Se expone un endpoint 
      `GET /api/v1/verificaciones/integridad/{uuid}` 
      de acceso público, no requiere autenticación.
- [ ] Al generar el certificado se calcula y almacena 
      su hash SHA-256 en la base de datos.
- [ ] La validación compara el hash del archivo actual 
      con el hash almacenado al momento de la emisión.
- [ ] Si los hashes coinciden se retorna íntegro en true.
- [ ] Si los hashes no coinciden se retorna íntegro en false.
- [ ] Si el UUID no existe se retorna error 404.

### 2. 📆 Estructura de la información

- [ ] La respuesta exitosa cuando el documento es íntegro 
      tiene la siguiente estructura:

```json
{
  "success": true,
  "statusCode": 200,
  "message": "Integridad del certificado verificada",
  "data": {
    "uuid": "550e8400",
    "integro": true,
    "fecha_emision": "2026-03-18",
    "mensaje": "El documento no ha sido alterado desde su emisión"
  }
}
```

- [ ] Si el documento fue alterado, el backend retorna:

```json
{
  "success": true,
  "statusCode": 200,
  "message": "Integridad del certificado verificada",
  "data": {
    "uuid": "550e8400",
    "integro": false,
    "fecha_emision": "2026-03-18",
    "mensaje": "El documento ha sido modificado y no es confiable"
  }
}
```

- [ ] Si el UUID no existe, el backend retorna:

```json
{
  "success": false,
  "statusCode": 404,
  "message": "No fue posible verificar la integridad",
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
| `GET` | `/api/v1/verificaciones/integridad/{uuid}` | Valida integridad del certificado por UUID |

### 📤 Ejemplo de Respuesta JSON

```json
{
  "success": true,
  "statusCode": 200,
  "message": "Integridad del certificado verificada",
  "data": {
    "uuid": "550e8400",
    "integro": true,
    "fecha_emision": "2026-03-18",
    "mensaje": "El documento no ha sido alterado desde su emisión"
  }
}
```

## 🧪 Requisitos de Pruebas

### 🔍 Casos de Prueba Funcional

### ✅ Caso 1: Documento íntegro

- **Precondición:** El UUID existe y el archivo PDF no ha 
  sido modificado desde su emisión.
- **Acción:** Ejecutar 
  `GET /api/v1/verificaciones/integridad/550e8400` sin token.
- **Resultado esperado:**
  - Código HTTP 200 OK
  - Campo `integro` igual a `true`
  - Campo `mensaje` indica que el documento no fue alterado

### ✅ Caso 2: Documento alterado

- **Precondición:** El UUID existe pero el archivo PDF fue 
  modificado después de su emisión.
- **Acción:** Ejecutar 
  `GET /api/v1/verificaciones/integridad/550e8400`.
- **Resultado esperado:**
  - Código HTTP 200 OK
  - Campo `integro` igual a `false`
  - Campo `mensaje` indica que el documento fue modificado 
    y no es confiable

### ❌ Caso 3: UUID no encontrado

- **Precondición:** No existe ningún certificado con el 
  UUID proporcionado.
- **Acción:** Ejecutar 
  `GET /api/v1/verificaciones/integridad/uuid-inexistente`.
- **Resultado esperado:**
  - Código HTTP 404 Not Found
  - Campo `details` indica que el certificado no existe

### ❌ Caso 4: UUID con formato inválido

- **Precondición:** El verificador ingresa un UUID con 
  formato incorrecto.
- **Acción:** Ejecutar 
  `GET /api/v1/verificaciones/integridad/123`.
- **Resultado esperado:**
  - Código HTTP 400 Bad Request
  - Campo `details` indica que el formato del UUID 
    no es válido

## ✅ Definición de Hecho

### 📦 Alcance Funcional

- [ ] El hash SHA-256 se calcula y almacena al momento 
      de generar el certificado.
- [ ] El endpoint compara correctamente el hash actual 
      con el hash almacenado.
- [ ] El acceso es público, no requiere autenticación.
- [ ] Retorna íntegro en false cuando el archivo fue alterado.
- [ ] La respuesta JSON cumple con el contrato definido.

### 🧪 Pruebas Completadas

- [ ] Se ejecutaron pruebas para documento íntegro y 
      documento alterado.
- [ ] Se probó con UUID inexistente y formato inválido.
- [ ] Las pruebas funcionales están documentadas y pasadas.

### 📄 Documentación Técnica

- [ ] Endpoint documentado en Swagger / OpenAPI.
- [ ] Se describe:
  - Propósito del endpoint
  - Cómo funciona la validación por hash SHA-256
  - Ejemplo de respuesta para documento íntegro
  - Ejemplo de respuesta para documento alterado
  - Ejemplo de error

### 🔐 Manejo de Errores

- [ ] Se retorna HTTP 404 cuando el UUID no existe.
- [ ] Se retorna HTTP 400 cuando el UUID tiene formato inválido.
- [ ] El campo `message` incluye texto claro en todos los 
      casos de error.