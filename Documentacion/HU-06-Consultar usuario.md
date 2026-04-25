# [HU-06] Consultar usuario

## 📖 Historia de Usuario

**Como** administrador del sistema

**Quiero** consultar la información de un usuario registrado buscándolo por su id

**Para** revisar sus datos de perfil y estado dentro del sistema antes de realizar cualquier gestión sobre su cuenta.

## 🔁 Flujo Esperado

- El cliente envía una petición GET al endpoint 
  ``/api/v1/usuarios/{id}`` con el id del usuario 
  como parámetro de ruta.
- El sistema consume el endpoint `GET /api/v1/usuarios/{id}` 
  con el id del usuario.
- El backend valida que el usuario con ese id exista en 
  el sistema.
- Si existe, se retorna la información completa del usuario.

## ✅ Criterios de Aceptación

### 1. 🔍 Estructura y lógica del servicio

- [ ] Se expone un endpoint `GET /api/v1/usuarios/{id}` accesible 
      solo para rol ADMINISTRADOR.
- [ ] Se valida que el usuario con el id proporcionado exista 
      en el sistema.
- [ ] La respuesta incluye nombre, correo, rol y estado activo 
      del usuario.

### 2. 📆 Estructura de la información

- [ ] La respuesta exitosa tiene la siguiente estructura:

```json
{
  "success": true,
  "statusCode": 200,
  "message": "Usuario encontrado",
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
  "message": "No fue posible consultar el usuario",
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
| `GET` | `/api/v1/usuarios/{id}` | Obtiene la información de un usuario específico |

### 📤 Ejemplo de Respuesta JSON

```json
{
  "success": true,
  "statusCode": 200,
  "message": "Usuario encontrado",
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

### ✅ Caso 1: Consulta exitosa

- **Precondición:** El administrador está autenticado y el usuario 
  con el id proporcionado existe en el sistema.
- **Acción:** Ejecutar `GET /api/v1/usuarios/1` con token 
  de administrador.
- **Resultado esperado:**
  - Código HTTP 200 OK
  - Campo `success` igual a `true`
  - Se retornan nombre, correo, rol y estado del usuario

### ❌ Caso 2: Usuario no encontrado

- **Precondición:** No existe ningún usuario con el id proporcionado.
- **Acción:** Ejecutar `GET /api/v1/usuarios/999` con token 
  de administrador.
- **Resultado esperado:**
  - Código HTTP 404 Not Found
  - Campo `details` indica que el usuario no existe

### ❌ Caso 3: Acceso sin rol administrador

- **Precondición:** Un usuario con rol ESTUDIANTE intenta 
  consultar otro usuario.
- **Acción:** Ejecutar `GET /api/v1/usuarios/1` con token 
  de estudiante.
- **Resultado esperado:**
  - Código HTTP 403 Forbidden
  - Campo `details` indica que no tiene permisos

## ✅ Definición de Hecho

### 📦 Alcance Funcional

- [ ] El endpoint retorna correctamente la información del usuario.
- [ ] Responde con 404 cuando el usuario no existe.
- [ ] Solo el administrador puede ejecutar este endpoint.
- [ ] La respuesta JSON cumple con el contrato definido.

### 🧪 Pruebas Completadas

- [ ] Se ejecutaron pruebas unitarias para usuario existente 
      e inexistente.
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
- [ ] Se retorna HTTP 403 cuando el rol no tiene permiso.
- [ ] El campo `message` incluye texto claro en todos los 
      casos de error.