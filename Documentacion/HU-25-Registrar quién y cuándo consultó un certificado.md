# [HU-25] Registrar consulta de verificación

## 📖 Historia de Usuario

**Como** sistema de verificación

**Quiero** registrar automáticamente cada consulta de 
verificación guardando el UUID consultado, timestamp 
e IP del verificador

**Para** mantener un historial de auditoría que permita 
a la universidad saber cuántas veces y desde dónde 
fue verificado cada certificado.

## 🔁 Flujo Esperado

- El verificador consulta un certificado mediante 
  HU-19 verificar validez.
- Automáticamente el sistema consume el endpoint 
  `POST /api/v1/verificaciones/consultas` internamente.
- El backend guarda el UUID consultado, timestamp 
  e IP del verificador.
- El registro no afecta ni retrasa la respuesta 
  al verificador.
- Solo el administrador puede consultar el historial 
  de verificaciones.

## ✅ Criterios de Aceptación

### 1. 🔍 Estructura y lógica del servicio

- [ ] Se expone un endpoint 
      `POST /api/v1/verificaciones/consultas` que se 
      ejecuta automáticamente tras cada verificación.
- [ ] El registro guarda UUID consultado, timestamp 
      e IP del verificador.
- [ ] El registro se guarda independientemente de si 
      el certificado existe o no.
- [ ] El administrador puede consultar el historial 
      de verificaciones con 
      `GET /api/v1/verificaciones/consultas`.
- [ ] El historial puede filtrarse por UUID para ver 
      cuántas veces fue verificado un certificado.

### 2. 📆 Estructura de la información

- [ ] El registro guardado tiene la siguiente estructura:

```json
{
  "success": true,
  "statusCode": 201,
  "message": "Consulta registrada correctamente",
  "data": {
    "id": 1,
    "uuid_consultado": "550e8400",
    "ip_verificador": "192.168.1.1",
    "timestamp": "2026-03-18T10:00:00Z"
  }
}
```

- [ ] La respuesta del historial de verificaciones tiene 
      la siguiente estructura:

```json
{
  "success": true,
  "statusCode": 200,
  "message": "Historial de verificaciones encontrado",
  "data": [
    {
      "id": 1,
      "uuid_consultado": "550e8400",
      "ip_verificador": "192.168.1.1",
      "timestamp": "2026-03-18T10:00:00Z"
    },
    {
      "id": 2,
      "uuid_consultado": "550e8400",
      "ip_verificador": "192.168.1.2",
      "timestamp": "2026-03-19T11:00:00Z"
    }
  ]
}
```

## 🔧 Notas Técnicas

### 🚀 Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| `POST` | `/api/v1/verificaciones/consultas` | Registra automáticamente cada consulta de verificación |
| `GET` | `/api/v1/verificaciones/consultas` | Lista el historial de consultas, filtrable por UUID |

### 📤 Ejemplo de Respuesta JSON

```json
{
  "success": true,
  "statusCode": 201,
  "message": "Consulta registrada correctamente",
  "data": {
    "id": 1,
    "uuid_consultado": "550e8400",
    "ip_verificador": "192.168.1.1",
    "timestamp": "2026-03-18T10:00:00Z"
  }
}
```

## 🧪 Requisitos de Pruebas

### 🔍 Casos de Prueba Funcional

### ✅ Caso 1: Registro automático exitoso

- **Precondición:** El verificador consulta un certificado 
  mediante HU-19.
- **Acción:** Ejecutar `GET /api/v1/verificaciones/550e8400`.
- **Resultado esperado:**
  - El registro se guarda automáticamente con UUID, 
    timestamp e IP
  - La respuesta al verificador no se ve afectada

### ✅ Caso 2: Registro de consulta con UUID inexistente

- **Precondición:** El verificador consulta un UUID que 
  no existe en el sistema.
- **Acción:** Ejecutar 
  `GET /api/v1/verificaciones/uuid-inexistente`.
- **Resultado esperado:**
  - El registro se guarda igualmente con el UUID 
    consultado, timestamp e IP
  - La respuesta retorna 404 al verificador normalmente

### ✅ Caso 3: Administrador consulta historial

- **Precondición:** El administrador está autenticado y 
  existen registros de verificaciones.
- **Acción:** Ejecutar `GET /api/v1/verificaciones/consultas` 
  con token de administrador.
- **Resultado esperado:**
  - Código HTTP 200 OK
  - Campo `data` contiene todos los registros de 
    verificaciones

### ✅ Caso 4: Administrador filtra historial por UUID

- **Precondición:** El administrador está autenticado y 
  existen registros para el UUID consultado.
- **Acción:** Ejecutar 
  `GET /api/v1/verificaciones/consultas?uuid=550e8400`.
- **Resultado esperado:**
  - Código HTTP 200 OK
  - Campo `data` contiene solo registros del UUID 
    especificado

### ❌ Caso 5: Acceso al historial sin rol administrador

- **Precondición:** Un usuario con rol ESTUDIANTE intenta 
  consultar el historial de verificaciones.
- **Acción:** Ejecutar `GET /api/v1/verificaciones/consultas` 
  con token de estudiante.
- **Resultado esperado:**
  - Código HTTP 403 Forbidden
  - Campo `details` indica que no tiene permisos

## ✅ Definición de Hecho

### 📦 Alcance Funcional

- [ ] Cada verificación queda registrada automáticamente 
      con UUID, timestamp e IP.
- [ ] El registro se guarda aunque el UUID no exista.
- [ ] El administrador puede consultar el historial 
      completo de verificaciones.
- [ ] El historial puede filtrarse por UUID.
- [ ] La respuesta al verificador no se ve afectada 
      por el registro.
- [ ] La respuesta JSON cumple con el contrato definido.

### 🧪 Pruebas Completadas

- [ ] Se verificó que el registro se guarda automáticamente 
      tras cada verificación.
- [ ] Se probó el registro con UUID existente e inexistente.
- [ ] Se probó el historial con y sin filtro por UUID.
- [ ] Se probó el acceso al historial con rol no autorizado.
- [ ] Las pruebas funcionales están documentadas y pasadas.

### 📄 Documentación Técnica

- [ ] Endpoints documentados en Swagger / OpenAPI.
- [ ] Se describe:
  - Propósito del registro automático
  - Campos guardados en cada registro
  - Ejemplo de respuesta del historial
  - Ejemplo de error

### 🔐 Manejo de Errores

- [ ] Se retorna HTTP 403 cuando el rol no tiene permiso 
      para consultar el historial.
- [ ] El campo `message` incluye texto claro en todos los 
      casos de error.