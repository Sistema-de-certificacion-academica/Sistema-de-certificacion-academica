# [HU-16] Listar plantillas de certificado

## 📖 Historia de Usuario

**Como** administrador del sistema

**Quiero** consultar la lista de todas las plantillas de certificado disponibles en el sistema

**Para** conocer qué formatos existen antes de gestionar una solicitud o crear una nueva plantilla.

## 🔁 Flujo Esperado

- El administrador accede a la sección de plantillas 
  desde la interfaz.
- El sistema consume el endpoint `GET /api/v1/plantillas`.
- El backend retorna todas las plantillas registradas 
  en el sistema.
- Se muestra la lista con el id, nombre, tipo de certificado 
  y estado activo de cada plantilla.

## ✅ Criterios de Aceptación

### 1. 🔍 Estructura y lógica del servicio

- [ ] Se expone un endpoint `GET /api/v1/plantillas` accesible 
      solo para rol ADMINISTRADOR.
- [ ] El endpoint retorna todas las plantillas registradas 
      en el sistema.
- [ ] Si no hay plantillas registradas, retorna una lista vacía.

### 2. 📆 Estructura de la información

- [ ] La respuesta exitosa tiene la siguiente estructura:

```json
{
  "success": true,
  "statusCode": 200,
  "message": "Plantillas encontradas",
  "data": [
    {
      "id": 5,
      "nombre": "Plantilla certificado de estudio",
      "tipo_certificado": "CERTIFICADO_ESTUDIO",
      "activa": true
    },
    {
      "id": 6,
      "nombre": "Plantilla certificado de notas",
      "tipo_certificado": "CERTIFICADO_NOTAS",
      "activa": true
    }
  ]
}
```

- [ ] Si no hay plantillas registradas, el backend retorna:

```json
{
  "success": true,
  "statusCode": 200,
  "message": "No hay plantillas registradas en el sistema",
  "data": []
}
```

## 🔧 Notas Técnicas

### 🚀 Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/api/v1/plantillas` | Lista todas las plantillas del sistema |

### 📤 Ejemplo de Respuesta JSON

```json
{
  "success": true,
  "statusCode": 200,
  "message": "Plantillas encontradas",
  "data": [
    {
      "id": 5,
      "nombre": "Plantilla certificado de estudio",
      "tipo_certificado": "CERTIFICADO_ESTUDIO",
      "activa": true
    }
  ]
}
```

## 🧪 Requisitos de Pruebas

### 🔍 Casos de Prueba Funcional

### ✅ Caso 1: Listado exitoso con plantillas

- **Precondición:** El administrador está autenticado y existen 
  plantillas registradas en el sistema.
- **Acción:** Ejecutar `GET /api/v1/plantillas` con token 
  de administrador.
- **Resultado esperado:**
  - Código HTTP 200 OK
  - Campo `success` igual a `true`
  - Campo `data` contiene la lista de plantillas con 
    id, nombre, tipo y estado

### ✅ Caso 2: Listado exitoso sin plantillas

- **Precondición:** El administrador está autenticado y no 
  hay plantillas registradas.
- **Acción:** Ejecutar `GET /api/v1/plantillas`.
- **Resultado esperado:**
  - Código HTTP 200 OK
  - Campo `data` retorna un array vacío
  - Campo `message` indica que no hay plantillas registradas

### ❌ Caso 3: Acceso sin rol administrador

- **Precondición:** Un usuario con rol ESTUDIANTE intenta 
  listar las plantillas.
- **Acción:** Ejecutar `GET /api/v1/plantillas` con token 
  de estudiante.
- **Resultado esperado:**
  - Código HTTP 403 Forbidden
  - Campo `details` indica que no tiene permisos

### ❌ Caso 4: Petición sin token

- **Precondición:** Se envía la petición sin header 
  de autorización.
- **Acción:** Ejecutar `GET /api/v1/plantillas` sin token.
- **Resultado esperado:**
  - Código HTTP 401 Unauthorized
  - Campo `details` indica que se requiere autenticación

## ✅ Definición de Hecho

### 📦 Alcance Funcional

- [ ] El endpoint retorna correctamente la lista de plantillas.
- [ ] Retorna lista vacía cuando no hay plantillas registradas.
- [ ] Solo el administrador puede ejecutar este endpoint.
- [ ] La respuesta JSON cumple con el contrato definido.

### 🧪 Pruebas Completadas

- [ ] Se ejecutaron pruebas con plantillas existentes y 
      sin plantillas.
- [ ] Se probó el acceso con rol no autorizado.
- [ ] Se probó la petición sin token.
- [ ] Las pruebas funcionales están documentadas y pasadas.

### 📄 Documentación Técnica

- [ ] Endpoint documentado en Swagger / OpenAPI.
- [ ] Se describe:
  - Propósito del endpoint
  - Campos de salida
  - Ejemplo de respuesta exitosa con datos
  - Ejemplo de respuesta exitosa sin datos

### 🔐 Manejo de Errores

- [ ] Se retorna HTTP 403 cuando el rol no tiene permiso.
- [ ] Se retorna HTTP 401 cuando la petición llega sin token.
- [ ] El campo `message` incluye texto claro en todos los 
      casos de error.