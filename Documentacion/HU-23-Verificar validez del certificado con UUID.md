# [HU-23] Verificar validez del certificado mediante UUID

## 📖 Historia de Usuario

**Como** empresa o persona externa

**Quiero** verificar la validez de un certificado académico ingresando su código UUID sin necesidad de registrarme

**Para** confirmar que el documento es auténtico y fue emitido realmente por la universidad antes de tomar decisiones basadas en él.

## 🔁 Flujo Esperado

- El verificador ingresa el UUID del certificado en la 
  interfaz pública de verificación.
- El sistema consume el endpoint 
  `GET /api/v1/verificaciones/{codigo}` con el UUID.
- El backend busca el certificado en el repositorio 
  usando el UUID proporcionado.
- Si existe y es válido, retorna la información básica 
  del certificado sin exponer datos privados del estudiante.
- El sistema ejecuta automáticamente HU-25 para registrar la consulta con UUID, timestamp e IP del verificador

## ✅ Criterios de Aceptación

### 1. 🔍 Estructura y lógica del servicio

- [ ] Se expone un endpoint `GET /api/v1/verificaciones/{codigo}` 
      de acceso público, no requiere autenticación.
- [ ] El certificado se marca como válido solo si el UUID 
      existe en el repositorio y su estado es DISPONIBLE.
- [ ] Un certificado anulado retorna válido en false.
- [ ] El sistema no expone información privada del estudiante 
      como correo, contraseña o datos personales sensibles.
- [ ] Cada verificación dispara automáticamente el registro definido en HU-25

### 2. 📆 Estructura de la información

- [ ] La respuesta exitosa cuando el certificado es válido 
      tiene la siguiente estructura:

```json
{
  "success": true,
  "statusCode": 200,
  "message": "Certificado verificado correctamente",
  "data": {
    "valido": true,
    "uuid": "550e8400",
    "estudiante": "Erick Gutierrez",
    "tipo_certificado": "CERTIFICADO_ESTUDIO",
    "fecha_emision": "2026-03-18",
    "estado": "VIGENTE"
  }
}
```

- [ ] Si el certificado está anulado, el backend retorna:

```json
{
  "success": true,
  "statusCode": 200,
  "message": "Certificado no válido",
  "data": {
    "valido": false,
    "uuid": "550e8400",
    "estado": "ANULADO"
  }
}
```

- [ ] Si el UUID no existe, el backend retorna:

```json
{
  "success": false,
  "statusCode": 404,
  "message": "Certificado no encontrado",
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
| `GET` | `/api/v1/verificaciones/{codigo}` | Verifica la validez de un certificado por UUID |
| `POST` | `/api/v1/verificaciones/consultas` | Registra automáticamente cada consulta realizada |

### 📤 Ejemplo de Respuesta JSON

```json
{
  "success": true,
  "statusCode": 200,
  "message": "Certificado verificado correctamente",
  "data": {
    "valido": true,
    "uuid": "550e8400",
    "estudiante": "Erick Gutierrez",
    "tipo_certificado": "CERTIFICADO_ESTUDIO",
    "fecha_emision": "2026-03-18",
    "estado": "VIGENTE"
  }
}
```

## 🧪 Requisitos de Pruebas

### 🔍 Casos de Prueba Funcional

### ✅ Caso 1: Verificación exitosa certificado válido

- **Precondición:** El UUID existe en el repositorio y el 
  certificado está en estado DISPONIBLE.
- **Acción:** Ejecutar `GET /api/v1/verificaciones/550e8400` 
  sin token.
- **Resultado esperado:**
  - Código HTTP 200 OK
  - Campo `valido` igual a `true`
  - Campo `estado` igual a `VIGENTE`
  - Solo se muestra información básica del certificado

### ✅ Caso 2: Verificación de certificado anulado

- **Precondición:** El UUID existe pero el certificado 
  está anulado.
- **Acción:** Ejecutar `GET /api/v1/verificaciones/550e8400`.
- **Resultado esperado:**
  - Código HTTP 200 OK
  - Campo `valido` igual a `false`
  - Campo `estado` igual a `ANULADO`

### ✅ Caso 3: Consulta queda registrada automáticamente

- **Precondición:** Se realiza cualquier verificación 
  con un UUID válido.
- **Acción:** Ejecutar `GET /api/v1/verificaciones/550e8400`.
- **Resultado esperado:**
  - La consulta queda registrada con timestamp y UUID
  - El registro no afecta la respuesta al verificador

### ❌ Caso 4: UUID no encontrado

- **Precondición:** No existe ningún certificado con el 
  UUID proporcionado.
- **Acción:** Ejecutar 
  `GET /api/v1/verificaciones/uuid-inexistente`.
- **Resultado esperado:**
  - Código HTTP 404 Not Found
  - Campo `details` indica que el certificado no existe

### ❌ Caso 5: UUID con formato inválido

- **Precondición:** El verificador ingresa un UUID con 
  formato incorrecto.
- **Acción:** Ejecutar `GET /api/v1/verificaciones/123`.
- **Resultado esperado:**
  - Código HTTP 400 Bad Request
  - Campo `details` indica que el formato del UUID 
    no es válido

## ✅ Definición de Hecho

### 📦 Alcance Funcional

- [ ] El endpoint verifica correctamente la validez del 
      certificado por UUID.
- [ ] El acceso es público, no requiere autenticación.
- [ ] No expone información privada del estudiante.
- [ ] Certificados anulados retornan valido en false.
- [ ] Cada verificación queda registrada automáticamente.
- [ ] La respuesta JSON cumple con el contrato definido.

### 🧪 Pruebas Completadas

- [ ] Se ejecutaron pruebas para certificado válido, 
      anulado e inexistente.
- [ ] Se verificó que el registro de consulta se guarda 
      automáticamente.
- [ ] Se probó con UUID de formato inválido.
- [ ] Las pruebas funcionales están documentadas y pasadas.

### 📄 Documentación Técnica

- [ ] Endpoint documentado en Swagger / OpenAPI.
- [ ] Se describe:
  - Propósito del endpoint
  - Campos de entrada y salida
  - Ejemplo de respuesta para certificado válido
  - Ejemplo de respuesta para certificado anulado
  - Ejemplo de error

### 🔐 Manejo de Errores

- [ ] Se retorna HTTP 404 cuando el UUID no existe.
- [ ] Se retorna HTTP 400 cuando el UUID tiene formato inválido.
- [ ] El campo `message` incluye texto claro en todos los 
      casos de error.