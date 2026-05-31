# [HU-05] Actualizar perfil de usuario

## 📖 Historia de Usuario

**Como** administrador del sistema

**Quiero** actualizar la información de perfil de un usuario registrado

**Para** mantener los datos del sistema actualizados y corregir información incorrecta o desactualizada de cualquier usuario.

## 🔁 Flujo Esperado

- El cliente envía una petición PUT al endpoint 
  `/api/v1/usuarios/{id}` con los datos a actualizar en el cuerpo de la solicitud.
- El sistema consume el endpoint `PUT /api/v1/usuarios/{id}`con los datos a actualizar.
- El backend valida que el usuario exista en el sistema.
- El backend valida que si se cambia el correo, el nuevo correo no esté registrado por otro usuario.
- Si los datos son válidos, el perfil queda actualizado.
- Se retorna la información actualizada del usuario.

## ✅ Criterios de Aceptación

### 1. 🔍 Estructura y lógica del servicio

- [ ] Se expone un endpoint `PUT /api/v1/usuarios/{id}` accesible solo para rol ADMINISTRADOR.
- [ ] Se valida que el usuario con el id proporcionado exista en el sistema.
- [ ] Si se actualiza el correo, se valida que no esté en uso por otro usuario.
- [ ] El rol solo puede ser ESTUDIANTE o ADMINISTRADOR.
- [ ] Si la petición incluye el campo activo, el sistema lo ignora y no modifica el estado del usuario.

### 2. 📆 Estructura de la información

- [ ] La respuesta exitosa tiene la siguiente estructura:

```json
{
  "success": true,
  "statusCode": 200,
  "message": "Usuario actualizado correctamente",
  "data": {
    "id": 1,
    "nombre": "Erick Gutierrez",
    "correo": "erick@gmail.com",
    "rol": "ESTUDIANTE",
    "activo": true
  }
}
```

- [ ] Si el usuario no existe, el backend retorna:

```json
{
  "success": false,
  "statusCode": 404,
  "message": "No fue posible actualizar el usuario",
  "error": {
    "error_code": "NOT_FOUND",
    "details": "No existe un usuario con el id proporcionado",
    "timestamp": "2026-03-18T10:00:00Z"
  }
}
```

## 🔧 Notas Técnicas

### 🚀 Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| `PUT` | `/api/v1/usuarios/{id}` | Actualiza la información de perfil de un usuario |

### 📤 Ejemplo de Respuesta JSON

```json
{
  "success": true,
  "statusCode": 200,
  "message": "Usuario actualizado correctamente",
  "data": {
    "id": 1,
    "nombre": "Erick Gutierrez",
    "correo": "erick@gmail.com",
    "rol": "ESTUDIANTE",
    "activo": true
  }
}
```

## 🧪 Requisitos de Pruebas

### 🔍 Casos de Prueba Funcional

### ✅ Caso 1: Actualización exitosa

- **Precondición:** El administrador está autenticado y el usuario 
  con el id proporcionado existe en el sistema.
- **Acción:** Ejecutar `PUT /api/v1/usuarios/1` con los datos 
  a actualizar.
- **Resultado esperado:**
  - Código HTTP 200 OK
  - Campo `success` igual a `true`
  - Los datos retornados reflejan los cambios realizados

### ❌ Caso 2: Usuario no encontrado

- **Precondición:** No existe ningún usuario con el id proporcionado.
- **Acción:** Ejecutar `PUT /api/v1/usuarios/999` con datos válidos.
- **Resultado esperado:**
  - Código HTTP 404 Not Found
  - Campo `details` indica que el usuario no existe

### ❌ Caso 3: Correo ya en uso por otro usuario

- **Precondición:** El administrador intenta cambiar el correo 
  de un usuario a uno que ya usa otro usuario.
- **Acción:** Ejecutar `PUT /api/v1/usuarios/1` con un correo 
  ya registrado.
- **Resultado esperado:**
  - Código HTTP 409 Conflict
  - Campo `details` indica que el correo ya está en uso

### ❌ Caso 4: Rol no permitido

- **Precondición:** El administrador envía un rol que no existe 
  en el sistema.
- **Acción:** Ejecutar `PUT /api/v1/usuarios/1` con rol "PROFESOR".
- **Resultado esperado:**
  - Código HTTP 400 Bad Request
  - Campo `details` indica que el rol no es válido

### ❌ Caso 5: Acceso sin rol administrador

- **Precondición:** Un usuario con rol ESTUDIANTE intenta 
  actualizar un perfil.
- **Acción:** Ejecutar `PUT /api/v1/usuarios/1` con token 
  de estudiante.
- **Resultado esperado:**
  - Código HTTP 403 Forbidden
  - Campo `details` indica que no tiene permisos

## ✅ Definición de Hecho

### 📦 Alcance Funcional

- [ ] El endpoint actualiza correctamente el perfil del usuario.
- [ ] No permite correos duplicados entre usuarios.
- [ ] Solo el administrador puede ejecutar este endpoint.
- [ ] La respuesta JSON cumple con el contrato definido.

### 🧪 Pruebas Completadas

- [ ] Se ejecutaron pruebas unitarias para validación de 
      correo duplicado y usuario inexistente.
- [ ] Se probó el acceso con rol no autorizado.
- [ ] Se probó actualización con rol inválido.
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
- [ ] Se retorna HTTP 409 cuando el correo ya está en uso.
- [ ] Se retorna HTTP 400 cuando el rol es inválido.
- [ ] Se retorna HTTP 403 cuando el rol no tiene permiso.
- [ ] El campo `message` incluye texto claro en todos los 
      casos de error.