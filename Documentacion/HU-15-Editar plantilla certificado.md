# [HU-15] Editar plantilla de certificado

## 📖 Historia de Usuario

**Como** administrador del sistema

**Quiero** editar una plantilla de certificado existente actualizando su nombre, campos dinámicos o tipo de certificado

**Para** corregir o mejorar los formatos de certificados sin necesidad de crear una plantilla nueva desde cero.

## 🔁 Flujo Esperado

- El cliente envía una petición PUT al endpoint 
  ``/api/v1/plantillas/{id}`` con los datos a actualizar en el cuerpo de la solicitud.
- El sistema consume el endpoint `PUT /api/v1/plantillas/{id}` 
  con los datos a actualizar.
- El backend valida que la plantilla exista en el sistema.
- El backend valida que la plantilla no haya sido usada 
  para generar certificados.
- Si las validaciones pasan, la plantilla queda actualizada.
- Se retorna la información de la plantilla con los 
  cambios aplicados.

## ✅ Criterios de Aceptación

### 1. 🔍 Estructura y lógica del servicio

- [ ] Se expone un endpoint `PUT /api/v1/plantillas/{id}` 
      accesible solo para rol ADMINISTRADOR.
- [ ] Se valida que la plantilla con el id proporcionado 
      exista en el sistema.
- [ ] Si la plantilla tiene al menos un certificado 
      generado asociado el sistema retorna HTTP 409 
      con mensaje descriptivo sin modificar ningún dato.
- [ ] La plantilla editada debe seguir teniendo al menos 
      un campo dinámico.
- [ ] El tipo de certificado actualizado debe ser uno de 
      los permitidos en el sistema.

### 2. 📆 Estructura de la información

- [ ] La respuesta exitosa tiene la siguiente estructura:

```json
{
  "success": true,
  "statusCode": 200,
  "message": "Plantilla actualizada correctamente",
  "data": {
    "id": 5,
    "nombre": "Plantilla certificado de estudio v2",
    "tipo_certificado": "CERTIFICADO_ESTUDIO",
    "estructura": {
      "campos": [
        "nombre_estudiante",
        "programa_academico",
        "fecha_emision",
        "codigo_estudiante"
      ]
    },
    "activa": true
  }
}
```

- [ ] Si la plantilla ya fue usada para generar certificados, 
      el backend retorna:

```json
{
  "success": false,
  "statusCode": 409,
  "message": "No fue posible editar la plantilla",
  "error": {
    "error_code": "CONFLICT",
    "details": "No se puede editar una plantilla que ya fue usada para generar certificados",
    "timestamp": "2026-03-18T10:00:00Z"
  }
}
```

- [ ] Si la plantilla no existe, el backend retorna:

```json
{
  "success": false,
  "statusCode": 404,
  "message": "No fue posible editar la plantilla",
  "error": {
    "error_code": "NOT_FOUND",
    "details": "No existe una plantilla con el id proporcionado",
    "timestamp": "2026-03-18T10:00:00Z"
  }
}
```

## 🔧 Notas Técnicas

### 🚀 Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| `PUT` | `/api/v1/plantillas/{id}` | Actualiza una plantilla de certificado existente |

### 📤 Ejemplo de Respuesta JSON

```json
{
  "success": true,
  "statusCode": 200,
  "message": "Plantilla actualizada correctamente",
  "data": {
    "id": 5,
    "nombre": "Plantilla certificado de estudio v2",
    "tipo_certificado": "CERTIFICADO_ESTUDIO",
    "estructura": {
      "campos": [
        "nombre_estudiante",
        "programa_academico",
        "fecha_emision",
        "codigo_estudiante"
      ]
    },
    "activa": true
  }
}
```

## 🧪 Requisitos de Pruebas

### 🔍 Casos de Prueba Funcional

### ✅ Caso 1: Edición exitosa

- **Precondición:** El administrador está autenticado y la 
  plantilla existe y no ha sido usada para generar certificados.
- **Acción:** Ejecutar `PUT /api/v1/plantillas/5` con los 
  datos actualizados.
- **Resultado esperado:**
  - Código HTTP 200 OK
  - Campo `success` igual a `true`
  - Los datos retornados reflejan los cambios realizados

### ❌ Caso 2: Plantilla ya usada en certificados

- **Precondición:** La plantilla ya fue utilizada para 
  generar al menos un certificado.
- **Acción:** Ejecutar `PUT /api/v1/plantillas/5` con 
  datos actualizados.
- **Resultado esperado:**
  - Código HTTP 409 Conflict
  - Campo `details` indica que la plantilla no puede 
    editarse porque ya fue usada

### ❌ Caso 3: Plantilla no encontrada

- **Precondición:** No existe ninguna plantilla con el 
  id proporcionado.
- **Acción:** Ejecutar `PUT /api/v1/plantillas/999`.
- **Resultado esperado:**
  - Código HTTP 404 Not Found
  - Campo `details` indica que la plantilla no existe

### ❌ Caso 4: Edición deja la plantilla sin campos dinámicos

- **Precondición:** El administrador envía la actualización 
  con el array de campos vacío.
- **Acción:** Ejecutar `PUT /api/v1/plantillas/5` con 
  `"campos": []`.
- **Resultado esperado:**
  - Código HTTP 400 Bad Request
  - Campo `details` indica que se requiere al menos un 
    campo dinámico

### ❌ Caso 5: Acceso sin rol administrador

- **Precondición:** Un usuario con rol ESTUDIANTE intenta 
  editar una plantilla.
- **Acción:** Ejecutar `PUT /api/v1/plantillas/5` con 
  token de estudiante.
- **Resultado esperado:**
  - Código HTTP 403 Forbidden
  - Campo `details` indica que no tiene permisos

## ✅ Definición de Hecho

### 📦 Alcance Funcional

- [ ] El endpoint actualiza correctamente la plantilla.
- [ ] No permite editar plantillas que ya generaron certificados.
- [ ] La plantilla editada mantiene al menos un campo dinámico.
- [ ] Solo el administrador puede ejecutar este endpoint.
- [ ] La respuesta JSON cumple con el contrato definido.

### 🧪 Pruebas Completadas

- [ ] Se ejecutaron pruebas para edición exitosa y plantilla 
      ya usada.
- [ ] Se probó la edición dejando la plantilla sin campos.
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

- [ ] Se retorna HTTP 409 cuando la plantilla ya fue usada 
      en certificados.
- [ ] Se retorna HTTP 404 cuando la plantilla no existe.
- [ ] Se retorna HTTP 400 cuando quedaría sin campos dinámicos.
- [ ] Se retorna HTTP 403 cuando el rol no tiene permiso.
- [ ] El campo `message` incluye texto claro en todos los 
      casos de error.