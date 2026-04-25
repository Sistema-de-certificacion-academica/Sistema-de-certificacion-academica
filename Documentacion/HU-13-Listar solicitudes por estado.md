# [HU-13] Listar solicitudes por estado

## 📖 Historia de Usuario

**Como** administrador del sistema

**Quiero** consultar la lista de todas las solicitudes de certificado filtrando por estado

**Para** gestionar eficientemente las solicitudes pendientes y llevar seguimiento de las aprobadas y rechazadas sin 
necesidad de buscarlas una por una.

## 🔁 Flujo Esperado

- El administrador accede a la sección de solicitudes 
  desde la interfaz.
- El sistema consume el endpoint `GET /api/v1/solicitudes` 
  con o sin filtro de estado.
- El backend retorna todas las solicitudes o solo las 
  del estado indicado.
- Se muestra la lista con id, usuario, tipo de certificado, 
  estado y fecha de cada solicitud.

## ✅ Criterios de Aceptación

### 1. 🔍 Estructura y lógica del servicio

- [ ] Se expone un endpoint `GET /api/v1/solicitudes` accesible 
      solo para rol ADMINISTRADOR.
- [ ] Sin parámetros retorna todas las solicitudes del sistema.
- [ ] Con parámetro `?estado=PENDIENTE` retorna solo las 
      solicitudes de ese estado.
- [ ] Los estados válidos para filtrar son PENDIENTE, 
      APROBADA y RECHAZADA.
- [ ] Si no hay solicitudes retorna lista vacía.

### 2. 📆 Estructura de la información

- [ ] La respuesta exitosa tiene la siguiente estructura:

```json
{
  "success": true,
  "statusCode": 200,
  "message": "Solicitudes encontradas",
  "data": [
    {
      "id": 10,
      "usuario_id": 1,
      "tipo_certificado": "CERTIFICADO_ESTUDIO",
      "estado": "PENDIENTE",
      "comprobante_pago": "REF-123",
      "fecha_solicitud": "2026-03-18"
    },
    {
      "id": 11,
      "usuario_id": 2,
      "tipo_certificado": "CERTIFICADO_ESTUDIO",
      "estado": "PENDIENTE",
      "comprobante_pago": "REF-456",
      "fecha_solicitud": "2026-03-19"
    }
  ]
}
```

- [ ] Si no hay solicitudes, el backend retorna:

```json
{
  "success": true,
  "statusCode": 200,
  "message": "No hay solicitudes registradas",
  "data": []
}
```

- [ ] Si el estado del filtro no es válido, el backend retorna:

```json
{
  "success": false,
  "statusCode": 400,
  "message": "No fue posible listar las solicitudes",
  "error": {
    "error_code": "BAD_REQUEST",
    "details": "El estado proporcionado no es válido",
    "timestamp": "2026-03-18T10:00:00Z"
  }
}
```

## 🔧 Notas Técnicas

### 🚀 Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/api/v1/solicitudes` | Lista todas las solicitudes, filtrable por estado |

### 📤 Ejemplo de Respuesta JSON

```json
{
  "success": true,
  "statusCode": 200,
  "message": "Solicitudes encontradas",
  "data": [
    {
      "id": 10,
      "usuario_id": 1,
      "tipo_certificado": "CERTIFICADO_ESTUDIO",
      "estado": "PENDIENTE",
      "comprobante_pago": "REF-123",
      "fecha_solicitud": "2026-03-18"
    }
  ]
}
```

## 🧪 Requisitos de Pruebas

### 🔍 Casos de Prueba Funcional

### ✅ Caso 1: Listado exitoso sin filtro

- **Precondición:** El administrador está autenticado y 
  existen solicitudes registradas.
- **Acción:** Ejecutar `GET /api/v1/solicitudes` con token 
  de administrador.
- **Resultado esperado:**
  - Código HTTP 200 OK
  - Campo `success` igual a `true`
  - Campo `data` contiene todas las solicitudes del sistema

### ✅ Caso 2: Listado exitoso con filtro por estado

- **Precondición:** El administrador está autenticado y 
  existen solicitudes en estado PENDIENTE.
- **Acción:** Ejecutar `GET /api/v1/solicitudes?estado=PENDIENTE`.
- **Resultado esperado:**
  - Código HTTP 200 OK
  - Campo `data` contiene solo solicitudes en estado PENDIENTE

### ✅ Caso 3: Listado exitoso sin solicitudes

- **Precondición:** El administrador está autenticado y 
  no hay solicitudes en el sistema.
- **Acción:** Ejecutar `GET /api/v1/solicitudes`.
- **Resultado esperado:**
  - Código HTTP 200 OK
  - Campo `data` retorna array vacío

### ❌ Caso 4: Filtro con estado no válido

- **Precondición:** El administrador envía un estado que 
  no existe en el sistema.
- **Acción:** Ejecutar `GET /api/v1/solicitudes?estado=CANCELADA`.
- **Resultado esperado:**
  - Código HTTP 400 Bad Request
  - Campo `details` indica que el estado no es válido

### ❌ Caso 5: Acceso sin rol administrador

- **Precondición:** Un usuario con rol ESTUDIANTE intenta 
  listar solicitudes.
- **Acción:** Ejecutar `GET /api/v1/solicitudes` con token 
  de estudiante.
- **Resultado esperado:**
  - Código HTTP 403 Forbidden
  - Campo `details` indica que no tiene permisos

## ✅ Definición de Hecho

### 📦 Alcance Funcional

- [ ] El endpoint retorna correctamente la lista de solicitudes.
- [ ] El filtro por estado funciona correctamente.
- [ ] Retorna lista vacía cuando no hay solicitudes.
- [ ] Solo el administrador puede ejecutar este endpoint.
- [ ] La respuesta JSON cumple con el contrato definido.

### 🧪 Pruebas Completadas

- [ ] Se ejecutaron pruebas sin filtro, con filtro válido 
      e inválido.
- [ ] Se probó el listado sin solicitudes registradas.
- [ ] Se probó el acceso con rol no autorizado.
- [ ] Las pruebas funcionales están documentadas y pasadas.

### 📄 Documentación Técnica

- [ ] Endpoint documentado en Swagger / OpenAPI.
- [ ] Se describe:
  - Propósito del endpoint
  - Parámetro opcional de filtro por estado
  - Ejemplo de respuesta exitosa con datos
  - Ejemplo de respuesta exitosa sin datos
  - Ejemplo de error

### 🔐 Manejo de Errores

- [ ] Se retorna HTTP 400 cuando el estado del filtro 
      no es válido.
- [ ] Se retorna HTTP 403 cuando el rol no tiene permiso.
- [ ] El campo `message` incluye texto claro en todos los 
      casos de error.