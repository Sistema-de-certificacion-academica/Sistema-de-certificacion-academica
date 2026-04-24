# [HU-04] Registrar usuario en el sistema

## 📖 Historia de Usuario

**Como** administrador del sistema,

**Quiero** registrar nuevos usuarios ingresando su información básica 
y asignándoles un rol,

**Para** habilitar su acceso a la plataforma de forma controlada según 
el perfil que les corresponde dentro de la universidad.

## 🔁 Flujo Esperado

- El administrador ingresa los datos del nuevo usuario desde la interfaz.
- El sistema consume el endpoint `POST /api/v1/usuarios` con la 
  información del usuario.
- El backend valida que el correo no esté registrado previamente.
- El backend valida que el rol asignado sea uno de los permitidos.
- Si los datos son válidos, el usuario queda registrado y activo en 
  el sistema.
- Se retorna la información del usuario creado con su id asignado.

## ✅ Criterios de Aceptación

### 1. 🔍 Estructura y lógica del servicio

- [ ] Se expone un endpoint `POST /api/v1/usuarios` accesible solo 
      para rol ADMINISTRADOR.
- [ ] Se valida que el correo no esté registrado previamente en 
      el sistema.
- [ ] El rol asignado debe ser únicamente ESTUDIANTE, ADMINISTRADOR 
      o EMPRESA_EXTERNA.
- [ ] El usuario queda activo por defecto al momento del registro.
- [ ] Los campos nombre, correo, password y rol son obligatorios.

### 2. 📆 Estructura de la información

- [ ] La respuesta exitosa tiene la siguiente estructura:

```json
{
  "success": true,
  "statusCode": 201,
  "message": "Usuario registrado correctamente",
  "data": {
    "id": 1,
    "nombre": "Erick Gutierrez",
    "correo": "erick@gmail.com",
    "rol": "ESTUDIANTE",
    "activo": true
  }
}
```

- [ ] Si el correo ya existe, el backend retorna:

```json
{
  "success": false,
  "statusCode": 409,
  "message": "No fue posible registrar el usuario",
  "error": {
    "error_code": "CONFLICT",
    "details": "Ya existe un usuario registrado con ese correo",
    "timestamp": "2026-03-18T10:00:00Z"
  }
}
```

## 🔧 Notas Técnicas

### 🚀 Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| `POST` | `/api/v1/usuarios` | Registra un nuevo usuario en el sistema |

### 📤 Ejemplo de Respuesta JSON

```json
{
  "success": true,
  "statusCode": 201,
  "message": "Usuario registrado correctamente",
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

### ✅ Caso 1: Registro exitoso

- **Precondición:** El administrador está autenticado y el correo 
  no existe en el sistema.
- **Acción:** Ejecutar `POST /api/v1/usuarios` con nombre, correo, 
  password y rol válidos.
- **Resultado esperado:**
  - Código HTTP 201 Created
  - Campo `success` igual a `true`
  - Campo `id` presente y asignado automáticamente
  - Campo `activo` igual a `true`

### ❌ Caso 2: Correo duplicado

- **Precondición:** Ya existe un usuario con el mismo correo 
  en el sistema.
- **Acción:** Ejecutar `POST /api/v1/usuarios` con un correo 
  ya registrado.
- **Resultado esperado:**
  - Código HTTP 409 Conflict
  - Campo `details` indica que el correo ya está registrado

### ❌ Caso 3: Rol no permitido

- **Precondición:** El administrador envía un rol que no existe 
  en el sistema.
- **Acción:** Ejecutar `POST /api/v1/usuarios` con rol 
  por ejemplo "PROFESOR".
- **Resultado esperado:**
  - Código HTTP 400 Bad Request
  - Campo `details` indica que el rol no es válido

### ❌ Caso 4: Campos obligatorios vacíos

- **Precondición:** El administrador envía la petición sin 
  algún campo requerido.
- **Acción:** Ejecutar `POST /api/v1/usuarios` sin el campo correo.
- **Resultado esperado:**
  - Código HTTP 400 Bad Request
  - Campo `details` indica qué campo es obligatorio y falta

### ❌ Caso 5: Acceso sin rol administrador

- **Precondición:** Un usuario con rol ESTUDIANTE intenta 
  registrar un nuevo usuario.
- **Acción:** Ejecutar `POST /api/v1/usuarios` con token 
  de estudiante.
- **Resultado esperado:**
  - Código HTTP 403 Forbidden
  - Campo `details` indica que no tiene permisos

## ✅ Definición de Hecho

### 📦 Alcance Funcional

- [ ] El endpoint registra correctamente usuarios con rol válido.
- [ ] No permite registrar correos duplicados en el sistema.
- [ ] Solo el administrador puede ejecutar este endpoint.
- [ ] La respuesta JSON cumple con el contrato definido.

### 🧪 Pruebas Completadas

- [ ] Se ejecutaron pruebas unitarias para validación de correo 
      duplicado y rol inválido.
- [ ] Se probó el acceso con rol no autorizado.
- [ ] Se probaron campos obligatorios vacíos.
- [ ] Las pruebas funcionales están documentadas y pasadas.

### 📄 Documentación Técnica

- [ ] Endpoint documentado en Swagger / OpenAPI.
- [ ] Se describe:
  - Propósito del endpoint
  - Campos de entrada y salida
  - Ejemplo de respuesta exitosa
  - Ejemplo de error

### 🔐 Manejo de Errores

- [ ] Se retorna HTTP 409 cuando el correo ya está registrado.
- [ ] Se retorna HTTP 400 cuando los datos son inválidos o incompletos.
- [ ] Se retorna HTTP 403 cuando el rol no tiene permiso.
- [ ] El campo `message` incluye texto claro en todos los 
      casos de error.