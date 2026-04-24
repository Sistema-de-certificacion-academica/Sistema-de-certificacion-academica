# [HU-03] Validación de permisos y niveles de acceso por rol

## 📖 Historia de Usuario

**Como** usuario autenticado en el sistema,

**Quiero** que el sistema valide mi rol antes de permitirme acceder 
a cada funcionalidad

**Para** que solo pueda realizar las acciones que corresponden a mi 
perfil y se proteja la información de otros usuarios y procesos.

## 🔁 Flujo Esperado

- El usuario realiza cualquier petición al sistema con su token JWT.
- El sistema extrae el rol del usuario desde el token antes de 
  procesar la petición.
- El backend verifica que el rol tenga permiso para acceder al 
  endpoint solicitado.
- Si el rol es válido para esa ruta, se procesa la petición normalmente.
- Si el rol no tiene permiso, el sistema rechaza la petición con 
  HTTP 403 sin ejecutar ninguna lógica de negocio.

## ✅ Criterios de Aceptación

### 1. 🔍 Estructura y lógica del servicio

- [ ] Cada endpoint del sistema valida el rol del token antes de 
      ejecutarse.
- [ ] Los roles existentes son únicamente: ESTUDIANTE, ADMINISTRADOR 
      y EMPRESA_EXTERNA.
- [ ] Un ESTUDIANTE no puede acceder a endpoints exclusivos de 
      ADMINISTRADOR ni de EMPRESA_EXTERNA.
- [ ] Una EMPRESA_EXTERNA solo puede acceder a los endpoints del 
      módulo de verificación.
- [ ] Un ADMINISTRADOR puede acceder a la gestión de usuarios, 
      plantillas y solicitudes.

### 2. 📆 Estructura de la información

- [ ] Si el rol no tiene permiso, el backend retorna:

```json
{
  "success": false,
  "statusCode": 403,
  "message": "Acceso denegado",
  "error": {
    "error_code": "FORBIDDEN",
    "details": "No tiene permisos para acceder a este recurso",
    "timestamp": "2026-03-18T10:00:00Z"
  }
}
```

- [ ] Si la petición llega sin token, el backend retorna:

```json
{
  "success": false,
  "statusCode": 401,
  "message": "No autenticado",
  "error": {
    "error_code": "UNAUTHORIZED",
    "details": "Se requiere token de acceso para este recurso",
    "timestamp": "2026-03-18T10:00:00Z"
  }
}
```

## 🔧 Notas Técnicas

### 🚀 Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/api/v1/auth/validar` | Valida token vigente y retorna rol del usuario |

### 📤 Ejemplo de Respuesta JSON

```json
{
  "success": true,
  "statusCode": 200,
  "message": "Token válido",
  "data": {
    "id": 1,
    "nombre": "Erick Gutierrez",
    "correo": "erick@gmail.com",
    "rol": "ESTUDIANTE"
  }
}
```

## 🧪 Requisitos de Pruebas

### 🔍 Casos de Prueba Funcional

### ✅ Caso 1: Acceso permitido según rol

- **Precondición:** Usuario autenticado con rol ESTUDIANTE y token válido.
- **Acción:** Ejecutar `GET /api/v1/solicitudes/{id}` con el token.
- **Resultado esperado:**
  - Código HTTP 200 OK
  - El sistema procesa la petición normalmente

### ✅ Caso 2: Administrador accede a gestión de usuarios

- **Precondición:** Usuario autenticado con rol ADMINISTRADOR.
- **Acción:** Ejecutar `GET /api/v1/usuarios/{id}` con el token.
- **Resultado esperado:**
  - Código HTTP 200 OK
  - El sistema retorna la información del usuario solicitado

### ❌ Caso 3: Estudiante intenta acceder a gestión de usuarios

- **Precondición:** Usuario autenticado con rol ESTUDIANTE.
- **Acción:** Ejecutar `GET /api/v1/usuarios/{id}` con el token 
  de un estudiante.
- **Resultado esperado:**
  - Código HTTP 403 Forbidden
  - Campo `details` indica que no tiene permisos para ese recurso

### ❌ Caso 4: Empresa externa intenta crear una solicitud

- **Precondición:** Usuario autenticado con rol EMPRESA_EXTERNA.
- **Acción:** Ejecutar `POST /api/v1/solicitudes` con el token 
  de empresa.
- **Resultado esperado:**
  - Código HTTP 403 Forbidden
  - Campo `details` indica que no tiene permisos para ese recurso

### ❌ Caso 5: Petición sin token

- **Precondición:** El cliente envía una petición a cualquier 
  endpoint protegido sin token.
- **Acción:** Ejecutar cualquier endpoint sin header `Authorization`.
- **Resultado esperado:**
  - Código HTTP 401 Unauthorized
  - Campo `details` indica que se requiere autenticación

## ✅ Definición de Hecho

### 📦 Alcance Funcional

- [ ] Todos los endpoints validan el rol antes de ejecutar 
      cualquier lógica.
- [ ] Los tres roles tienen acceso correctamente delimitado.
- [ ] La respuesta JSON cumple con el contrato definido en 
      todos los casos.

### 🧪 Pruebas Completadas

- [ ] Se probó acceso permitido para cada rol en sus endpoints 
      correspondientes.
- [ ] Se probaron intentos de acceso con rol incorrecto.
- [ ] Se probó el comportamiento sin token en endpoints protegidos.
- [ ] Las pruebas funcionales están documentadas y pasadas.

### 📄 Documentación Técnica

- [ ] Lógica de validación de roles documentada en Swagger / OpenAPI.
- [ ] Se describe:
  - Roles disponibles y sus permisos por módulo
  - Respuesta esperada para acceso denegado
  - Ejemplo de error por rol incorrecto

### 🔐 Manejo de Errores

- [ ] Se retorna HTTP 403 cuando el rol no tiene permiso.
- [ ] Se retorna HTTP 401 cuando la petición llega sin token.
- [ ] El campo `message` incluye texto claro en todos los 
      casos de error.