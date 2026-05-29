# [HU-04] Registrar usuario en el sistema

## 📖 Historia de Usuario

**Como** administrador del sistema

**Quiero** registrar nuevos usuarios ingresando su información básica 
y asignándoles un rol, y permitir que estudiantes se registren 
de forma autónoma

**Para** habilitar el acceso a la plataforma de forma controlada según 
el perfil que corresponde a cada actor del sistema.

## 🔁 Flujo Esperado

- Para registro de administradores o empresas el cliente envía una 
  petición POST al endpoint /api/v1/usuarios con token de administrador.
- Para registro de estudiantes el cliente envía una petición POST 
  al endpoint /api/v1/usuarios/registro sin autenticación.
- El backend valida que el correo no esté registrado previamente.
- El backend valida que el rol asignado sea uno de los permitidos.
- El endpoint /api/v1/usuarios/registro solo acepta rol ESTUDIANTE.
- Si los datos son válidos, el usuario queda registrado y activo 
  en el sistema.
- Se retorna la información del usuario creado con su id asignado.

## ✅ Criterios de Aceptación

### 1. 🔍 Estructura y lógica del servicio

- [ ] Se expone un endpoint `POST /api/v1/usuarios` accesible solo 
      para rol ADMINISTRADOR.
- [ ] Se expone un endpoint público `POST /api/v1/usuarios/registro` 
      sin autenticación, solo acepta rol ESTUDIANTE.
- [ ] Si el endpoint /api/v1/usuarios/registro recibe un rol diferente 
      a ESTUDIANTE el sistema retorna HTTP 400.
- [ ] Se valida que el correo no esté registrado previamente en 
      el sistema.
- [ ] El rol asignado debe ser únicamente ESTUDIANTE, ADMINISTRADOR 
      o EMPRESA_EXTERNA.
- [ ] El usuario queda activo por defecto al momento del registro.
- [ ] Los campos nombre, correo, password y rol son obligatorios.
- [ ] El sistema inicializa con un usuario administrador por defecto 
      con correo admin@unicert.com para permitir el primer acceso.

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

- [ ] Si el endpoint de registro recibe un rol diferente a ESTUDIANTE 
      el backend retorna:

```json
{
  "success": false,
  "statusCode": 400,
  "message": "No fue posible registrar el usuario",
  "error": {
    "error_code": "BAD_REQUEST",
    "details": "El endpoint de registro solo acepta rol ESTUDIANTE",
    "timestamp": "2026-03-18T10:00:00Z"
  }
}
```

## 🔧 Notas Técnicas

### 🚀 Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| `POST` | `/api/v1/usuarios` | Registra admins y empresas, requiere rol ADMINISTRADOR |
| `POST` | `/api/v1/usuarios/registro` | Registro público solo para estudiantes |

### 👤 Usuario administrador por defecto
El sistema inicializa con un usuario administrador predefinido 
para permitir el primer acceso al sistema:
- **Correo:** admin@unicert.com
- **Password:** admin123
- **Rol:** ADMINISTRADOR

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

### ✅ Caso 1: Registro exitoso por administrador

- **Precondición:** El administrador está autenticado y el correo 
  no existe en el sistema.
- **Acción:** Ejecutar `POST /api/v1/usuarios` con nombre, correo, 
  password y rol válidos.
- **Resultado esperado:**
  - Código HTTP 201 Created
  - Campo `success` igual a `true`
  - Campo `id` presente y asignado automáticamente
  - Campo `activo` igual a `true`

### ✅ Caso 2: Registro exitoso de estudiante

- **Precondición:** El correo no existe en el sistema.
- **Acción:** Ejecutar `POST /api/v1/usuarios/registro` con 
  nombre, correo, password y rol ESTUDIANTE sin token.
- **Resultado esperado:**
  - Código HTTP 201 Created
  - Campo `success` igual a `true`
  - Campo `rol` igual a `ESTUDIANTE`
  - Campo `activo` igual a `true`

### ❌ Caso 3: Correo duplicado

- **Precondición:** Ya existe un usuario con el mismo correo.
- **Acción:** Ejecutar `POST /api/v1/usuarios` con correo 
  ya registrado.
- **Resultado esperado:**
  - Código HTTP 409 Conflict
  - Campo `details` indica que el correo ya está registrado

### ❌ Caso 4: Rol no permitido en endpoint de registro

- **Precondición:** El cliente envía rol diferente a ESTUDIANTE 
  en el endpoint público.
- **Acción:** Ejecutar `POST /api/v1/usuarios/registro` con 
  rol ADMINISTRADOR.
- **Resultado esperado:**
  - Código HTTP 400 Bad Request
  - Campo `details` indica que solo se acepta rol ESTUDIANTE

### ❌ Caso 5: Campos obligatorios vacíos

- **Precondición:** El cliente envía la petición sin algún 
  campo requerido.
- **Acción:** Ejecutar `POST /api/v1/usuarios` sin el campo correo.
- **Resultado esperado:**
  - Código HTTP 400 Bad Request
  - Campo `details` indica qué campo obligatorio falta

### ❌ Caso 6: Acceso sin rol administrador

- **Precondición:** Un usuario con rol ESTUDIANTE intenta 
  registrar un nuevo usuario en el endpoint protegido.
- **Acción:** Ejecutar `POST /api/v1/usuarios` con token 
  de estudiante.
- **Resultado esperado:**
  - Código HTTP 403 Forbidden
  - Campo `details` indica que no tiene permisos

## ✅ Definición de Hecho

### 📦 Alcance Funcional

- [ ] El endpoint protegido registra correctamente admins y empresas.
- [ ] El endpoint público registra correctamente estudiantes.
- [ ] No permite registrar correos duplicados en el sistema.
- [ ] El endpoint público rechaza roles diferentes a ESTUDIANTE.
- [ ] El sistema inicializa con usuario administrador por defecto.
- [ ] La respuesta JSON cumple con el contrato definido.

### 🧪 Pruebas Completadas

- [ ] Se ejecutaron pruebas para registro exitoso por admin 
      y por estudiante.
- [ ] Se probó correo duplicado en ambos endpoints.
- [ ] Se probó rol inválido en endpoint público.
- [ ] Se probaron campos obligatorios vacíos.
- [ ] Se probó acceso sin rol administrador al endpoint protegido.
- [ ] Las pruebas funcionales están documentadas y pasadas.

### 📄 Documentación Técnica

- [ ] Endpoints documentados en Swagger / OpenAPI.
- [ ] Se describe:
  - Propósito de cada endpoint
  - Campos de entrada y salida
  - Ejemplo de respuesta exitosa
  - Ejemplo de error

### 🔐 Manejo de Errores

- [ ] Se retorna HTTP 409 cuando el correo ya está registrado.
- [ ] Se retorna HTTP 400 cuando los datos son inválidos o incompletos.
- [ ] Se retorna HTTP 400 cuando el endpoint público recibe 
      rol diferente a ESTUDIANTE.
- [ ] Se retorna HTTP 403 cuando el rol no tiene permiso 
      en el endpoint protegido.
- [ ] El campo `message` incluye texto claro en todos los 
      casos de error.