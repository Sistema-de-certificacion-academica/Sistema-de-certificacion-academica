# [HU-07] Eliminar usuario

## 📖 Historia de Usuario

**Como** administrador del sistema

**Quiero** eliminar un usuario registrado buscándolo por su id

**Para** retirar del sistema cuentas que ya no deben tener acceso a la plataforma, manteniendo la base de usuarios actualizada.

## 🔁 Flujo Esperado

- El administrador selecciona el usuario a eliminar desde 
  la interfaz.
- El sistema consume el endpoint `DELETE /api/v1/usuarios/{id}`.
- El backend valida que el usuario con ese id exista en 
  el sistema.
- El backend valida que el usuario no tenga solicitudes 
  activas o certificados en proceso antes de eliminarlo.
- Si las validaciones pasan, el usuario queda eliminado 
  del sistema.
- Se retorna confirmación de eliminación sin contenido.

## ✅ Criterios de Aceptación

### 1. 🔍 Estructura y lógica del servicio

- [ ] Se expone un endpoint `DELETE /api/v1/usuarios/{id}` 
      accesible solo para rol ADMINISTRADOR.
- [ ] Se valida que el usuario con el id proporcionado exista 
      en el sistema.
- [ ] No se puede eliminar un usuario que tenga solicitudes 
      de certificado en estado PENDIENTE.
- [ ] Un administrador no puede eliminarse a sí mismo.

### 2. 📆 Estructura de la información

- [ ] La respuesta exitosa retorna:

```json
{
  "success": true,
  "statusCode": 204,
  "message": "Usuario eliminado correctamente",
  "data": null
}
```

- [ ] Si el usuario no existe, el backend retorna:

```json
{
  "success": false,
  "statusCode": 404,
  "message": "No fue posible eliminar el usuario",
  "error": {
    "error_code": "NOT_FOUND",
    "details": "No existe un usuario con el id proporcionado",
    "timestamp": "2026-03-18T10:00:00Z"
  }
}
```

- [ ] Si el usuario tiene solicitudes pendientes, el backend retorna:

```json
{
  "success": false,
  "statusCode": 409,
  "message": "No fue posible eliminar el usuario",
  "error": {
    "error_code": "CONFLICT",
    "details": "El usuario tiene solicitudes de certificado pendientes",
    "timestamp": "2026-03-18T10:00:00Z"
  }
}
```

## 🔧 Notas Técnicas

### 🚀 Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| `DELETE` | `/api/v1/usuarios/{id}` | Elimina un usuario del sistema |

### 📤 Ejemplo de Respuesta JSON

```json
{
  "success": true,
  "statusCode": 204,
  "message": "Usuario eliminado correctamente",
  "data": null
}
```

## 🧪 Requisitos de Pruebas

### 🔍 Casos de Prueba Funcional

### ✅ Caso 1: Eliminación exitosa

- **Precondición:** El administrador está autenticado y el usuario 
  existe sin solicitudes pendientes.
- **Acción:** Ejecutar `DELETE /api/v1/usuarios/1` con token 
  de administrador.
- **Resultado esperado:**
  - Código HTTP 204 No Content
  - Campo `success` igual a `true`
  - El usuario ya no aparece en consultas posteriores

### ❌ Caso 2: Usuario no encontrado

- **Precondición:** No existe ningún usuario con el id proporcionado.
- **Acción:** Ejecutar `DELETE /api/v1/usuarios/999`.
- **Resultado esperado:**
  - Código HTTP 404 Not Found
  - Campo `details` indica que el usuario no existe

### ❌ Caso 3: Usuario con solicitudes pendientes

- **Precondición:** El usuario tiene una solicitud de certificado 
  en estado PENDIENTE.
- **Acción:** Ejecutar `DELETE /api/v1/usuarios/1`.
- **Resultado esperado:**
  - Código HTTP 409 Conflict
  - Campo `details` indica que tiene solicitudes pendientes

### ❌ Caso 4: Administrador intenta eliminarse a sí mismo

- **Precondición:** El administrador autenticado intenta eliminar 
  su propia cuenta.
- **Acción:** Ejecutar `DELETE /api/v1/usuarios/{id}` con su 
  propio id.
- **Resultado esperado:**
  - Código HTTP 400 Bad Request
  - Campo `details` indica que no puede eliminarse a sí mismo

### ❌ Caso 5: Acceso sin rol administrador

- **Precondición:** Un usuario con rol ESTUDIANTE intenta 
  eliminar un usuario.
- **Acción:** Ejecutar `DELETE /api/v1/usuarios/1` con token 
  de estudiante.
- **Resultado esperado:**
  - Código HTTP 403 Forbidden
  - Campo `details` indica que no tiene permisos

## ✅ Definición de Hecho

### 📦 Alcance Funcional

- [ ] El endpoint elimina correctamente el usuario del sistema.
- [ ] No permite eliminar usuarios con solicitudes pendientes.
- [ ] No permite que un administrador se elimine a sí mismo.
- [ ] Solo el administrador puede ejecutar este endpoint.
- [ ] La respuesta JSON cumple con el contrato definido.

### 🧪 Pruebas Completadas

- [ ] Se ejecutaron pruebas unitarias para usuario existente, 
      inexistente y con solicitudes pendientes.
- [ ] Se probó el intento de autoeliminación del administrador.
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

- [ ] Se retorna HTTP 404 cuando el usuario no existe.
- [ ] Se retorna HTTP 409 cuando tiene solicitudes pendientes.
- [ ] Se retorna HTTP 400 cuando intenta eliminarse a sí mismo.
- [ ] Se retorna HTTP 403 cuando el rol no tiene permiso.
- [ ] El campo `message` incluye texto claro en todos los 
      casos de error.