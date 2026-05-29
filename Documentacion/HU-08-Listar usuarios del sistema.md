# [HU-08] Listar usuarios del sistema

## 📖 Historia de Usuario

**Como** administrador del sistema

**Quiero** consultar la lista de todos los usuarios registrados con la opción de filtrar por rol

**Para** tener una visión completa de los usuarios del sistema y gestionar sus cuentas de forma eficiente.

## 🔁 Flujo Esperado

- El cliente envía una petición GET al endpoint 
  ``/api/v1/usuarios`` con o sin el parámetro 
  de filtro ?rol=ESTUDIANTE.
- El sistema consume el endpoint `GET /api/v1/usuarios` 
  con o sin filtro de rol.
- El backend retorna todos los usuarios registrados o 
  solo los del rol indicado.
- Se muestra la lista con id, nombre, correo, rol y 
  estado de cada usuario.

## ✅ Criterios de Aceptación

### 1. 🔍 Estructura y lógica del servicio

- [ ] Se expone un endpoint `GET /api/v1/usuarios` accesible 
      solo para rol ADMINISTRADOR.
- [ ] Sin parámetros retorna todos los usuarios del sistema.
- [ ] Con parámetro `?rol=ESTUDIANTE` retorna solo los 
      usuarios de ese rol.
- [ ] Los roles válidos para filtrar son ESTUDIANTE 
      y ADMINISTRADOR.
- [ ] Si no hay usuarios registrados el sistema retorna HTTP 200 con campo data como array vacío [].

### 2. 📆 Estructura de la información

- [ ] La respuesta exitosa tiene la siguiente estructura:

```json
{
  "success": true,
  "statusCode": 200,
  "message": "Usuarios encontrados",
  "data": [
    {
      "id": 1,
      "nombre": "Erick Gutierrez",
      "correo": "erick@gmail.com",
      "rol": "ESTUDIANTE",
      "activo": true
    },
    {
      "id": 2,
      "nombre": "Hansel Rodriguez",
      "correo": "mauricio@gmail.com",
      "rol": "ADMINISTRADOR",
      "activo": true
    }
  ]
}
```

- [ ] Si no hay usuarios registrados, el backend retorna:

```json
{
  "success": true,
  "statusCode": 200,
  "message": "No hay usuarios registrados en el sistema",
  "data": []
}
```

- [ ] Si el rol del filtro no es válido, el backend retorna:

```json
{
  "success": false,
  "statusCode": 400,
  "message": "No fue posible listar los usuarios",
  "error": {
    "error_code": "BAD_REQUEST",
    "details": "El rol proporcionado no es válido",
    "timestamp": "2026-03-18T10:00:00Z"
  }
}
```

## 🔧 Notas Técnicas

### 🚀 Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/api/v1/usuarios` | Lista todos los usuarios, filtrable por rol |

### 📤 Ejemplo de Respuesta JSON

```json
{
  "success": true,
  "statusCode": 200,
  "message": "Usuarios encontrados",
  "data": [
    {
      "id": 1,
      "nombre": "Erick Gutierrez",
      "correo": "erick@gmail.com",
      "rol": "ESTUDIANTE",
      "activo": true
    }
  ]
}
```

## 🧪 Requisitos de Pruebas

### 🔍 Casos de Prueba Funcional

### ✅ Caso 1: Listado exitoso sin filtro

- **Precondición:** El administrador está autenticado y 
  existen usuarios registrados.
- **Acción:** Ejecutar `GET /api/v1/usuarios` con token 
  de administrador.
- **Resultado esperado:**
  - Código HTTP 200 OK
  - Campo `success` igual a `true`
  - Campo `data` contiene todos los usuarios del sistema

### ✅ Caso 2: Listado exitoso con filtro por rol

- **Precondición:** El administrador está autenticado y 
  existen usuarios con rol ESTUDIANTE.
- **Acción:** Ejecutar `GET /api/v1/usuarios?rol=ESTUDIANTE`.
- **Resultado esperado:**
  - Código HTTP 200 OK
  - Campo `data` contiene solo usuarios con rol ESTUDIANTE

### ✅ Caso 3: Listado exitoso sin usuarios registrados

- **Precondición:** El administrador está autenticado y 
  no hay usuarios en el sistema.
- **Acción:** Ejecutar `GET /api/v1/usuarios`.
- **Resultado esperado:**
  - Código HTTP 200 OK
  - Campo `data` retorna array vacío

### ❌ Caso 4: Filtro con rol no válido

- **Precondición:** El administrador envía un rol que 
  no existe en el sistema.
- **Acción:** Ejecutar `GET /api/v1/usuarios?rol=PROFESOR`.
- **Resultado esperado:**
  - Código HTTP 400 Bad Request
  - Campo `details` indica que el rol no es válido

### ❌ Caso 5: Acceso sin rol administrador

- **Precondición:** Un usuario con rol ESTUDIANTE intenta 
  listar usuarios.
- **Acción:** Ejecutar `GET /api/v1/usuarios` con token 
  de estudiante.
- **Resultado esperado:**
  - Código HTTP 403 Forbidden
  - Campo `details` indica que no tiene permisos

## ✅ Definición de Hecho

### 📦 Alcance Funcional

- [ ] El endpoint retorna correctamente la lista de usuarios.
- [ ] El filtro por rol funciona correctamente.
- [ ] Retorna lista vacía cuando no hay usuarios registrados.
- [ ] Solo el administrador puede ejecutar este endpoint.
- [ ] La respuesta JSON cumple con el contrato definido.

### 🧪 Pruebas Completadas

- [ ] Se ejecutaron pruebas sin filtro, con filtro válido 
      e inválido.
- [ ] Se probó el listado sin usuarios registrados.
- [ ] Se probó el acceso con rol no autorizado.
- [ ] Las pruebas funcionales están documentadas y pasadas.

### 📄 Documentación Técnica

- [ ] Endpoint documentado en Swagger / OpenAPI.
- [ ] Se describe:
  - Propósito del endpoint
  - Parámetro opcional de filtro por rol
  - Ejemplo de respuesta exitosa con datos
  - Ejemplo de respuesta exitosa sin datos
  - Ejemplo de error

### 🔐 Manejo de Errores

- [ ] Se retorna HTTP 400 cuando el rol del filtro no 
      es válido.
- [ ] Se retorna HTTP 403 cuando el rol no tiene permiso.
- [ ] El campo `message` incluye texto claro en todos los 
      casos de error