# [HU-02] Cierre de sesión e invalidación del token

## 📖 Historia de Usuario

**Como** usuario autenticado en el sistema (estudiante, administrador o empresa externa)

**Quiero** cerrar mi sesión activa

**Para** garantizar que mi token de acceso quede invalidado y ningún tercero pueda usar mi sesión después de que yo la termine.

## 🔁 Flujo Esperado

- El usuario solicita cerrar sesión desde la interfaz.
- El sistema consume el endpoint `POST /api/v1/auth/logout` enviando 
  el token en el header `Authorization: Bearer {token}`.
- El backend valida que el token sea vigente y pertenezca a una sesión activa.
- El sistema invalida el token y lo marca como revocado.
- Se retorna confirmación de cierre de sesión exitoso.

## ✅ Criterios de Aceptación

### 1. 🔍 Estructura y lógica del servicio

- [ ] Se expone un endpoint `POST /api/v1/auth/logout` que recibe 
      el token en el header.
- [ ] El sistema valida que el token exista y esté activo antes de invalidarlo.
- [ ] Una vez revocado, el token no puede usarse en ninguna petición posterior.
- [ ] Si el token ya estaba revocado o expirado, el sistema responde con error.

### 2. 📆 Estructura de la información

- [ ] La respuesta exitosa tiene la siguiente estructura:

```json
{
  "success": true,
  "statusCode": 200,
  "message": "Sesión cerrada correctamente",
  "data": null
}
```

- [ ] Si el token es inválido o ya fue revocado, el backend retorna:

```json
{
  "success": false,
  "statusCode": 401,
  "message": "No se pudo cerrar la sesión",
  "error": {
    "error_code": "UNAUTHORIZED",
    "details": "El token proporcionado no es válido o ya fue revocado",
    "timestamp": "2026-03-18T10:00:00Z"
  }
}
```

## 🔧 Notas Técnicas

### 🚀 Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| `POST` | `/api/v1/auth/logout` | Cierra sesión e invalida el token activo |

### 📤 Ejemplo de Respuesta JSON

```json
{
  "success": true,
  "statusCode": 200,
  "message": "Sesión cerrada correctamente",
  "data": null
}
```

## 🧪 Requisitos de Pruebas

### 🔍 Casos de Prueba Funcional

### ✅ Caso 1: Logout exitoso

- **Precondición:** El usuario tiene una sesión activa con token válido.
- **Acción:** Ejecutar `POST /api/v1/auth/logout` con el token en el header.
- **Resultado esperado:**
  - Código HTTP 200 OK
  - Campo `success` igual a `true`
  - El token queda invalidado para peticiones posteriores

### ❌ Caso 2: Token ya revocado

- **Precondición:** El usuario intenta cerrar sesión con un token 
  que ya fue invalidado previamente.
- **Acción:** Ejecutar `POST /api/v1/auth/logout` con token revocado.
- **Resultado esperado:**
  - Código HTTP 401 Unauthorized
  - Campo `details` indica que el token ya fue revocado

### ❌ Caso 3: Petición sin token

- **Precondición:** El cliente envía la petición sin header de autorización.
- **Acción:** Ejecutar `POST /api/v1/auth/logout` sin header `Authorization`.
- **Resultado esperado:**
  - Código HTTP 401 Unauthorized
  - Campo `message` indica que se requiere autenticación

## ✅ Definición de Hecho

### 📦 Alcance Funcional

- [ ] El endpoint de logout invalida correctamente el token activo.
- [ ] Un token revocado no puede usarse en ninguna petición posterior.
- [ ] La respuesta JSON cumple con el contrato definido.

### 🧪 Pruebas Completadas

- [ ] Se ejecutaron pruebas unitarias para la revocación del token.
- [ ] Se cubrieron los casos de token ya revocado y petición sin token.
- [ ] Las pruebas funcionales están documentadas y pasadas.

### 📄 Documentación Técnica

- [ ] Endpoint documentado en Swagger / OpenAPI.
- [ ] Se describe:
  - Propósito del endpoint
  - Campos de entrada y salida
  - Ejemplo de respuesta exitosa
  - Ejemplo de error

### 🔐 Manejo de Errores

- [ ] Se retorna HTTP 401 cuando el token es inválido o ya fue revocado.
- [ ] Se retorna HTTP 401 cuando la petición llega sin token.
- [ ] El campo `message` incluye texto claro y amigable en todos 
      los casos de error.