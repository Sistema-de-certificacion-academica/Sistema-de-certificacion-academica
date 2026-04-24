# [HU-01] Autenticacion de usuario mediante credenciales

## 📖 Historia de Usuario

**Como** usuario del sistema (estudiante, administrador o empresa externa)

**Quiero** iniciar sesión con mi correo y contraseña y recibir un token de acceso válido

**Para** poder acceder a las funcionalidades del sistema según mi rol de forma segura y autenticada

## 🔁 Flujo Esperado
- El usuario ingresa su correo y contraseña en la interfaz de login.
- El sistema consume el endpoint POST /api/v1/auth/login con las credenciales.
- El backend valida que el usuario exista y no esté bloqueado o inactivo.
- Si las credenciales son correctas, el sistema genera un token JWT con duración de 24 horas.
- El token se retorna al cliente junto con el rol y datos básicos del usuario.
- El cliente almacena el token para usarlo en las siguientes peticiones como Authorization: Bearer {token}. 

## ✅ Criterios de Aceptación

### 1. 🔍 Estructura y lógica del servicio

- [ ] Se expone un endpoint POST /api/v1/auth/login que recibe correo y contraseña
- [ ] Se valida que el correo exista en el sistema antes de comparar la contraseña.
- [ ] El token JWT generado tiene una duración máxima de 24 horas.
- [ ] Después de 5 intentos fallidos consecutivos la cuenta se bloquea temporalmente

### 2. 📆 Estructura de la información

-[ ] La respuesta exitosa tiene la siguiente estructura: 
```json
{
  "success": true,
  "statusCode": 200,
  "message": "Inicio de sesión exitoso",
  "data": {
    "token": "eyJhbGciOiJI",
    "tipo_token": "Bearer",
    "usuario": {
      "id": 1,
      "nombre": "Erick Gutierrez",
      "correo": "erick@gmail.com",
      "rol": "ESTUDIANTE"
    }
  }
}
```
-[ ] Si las credenciales son incorrectas, el backend retorna:
```json
{
  "success": false,
  "statusCode": 401,
  "message": "No se pudo iniciar sesión",
  "error": {
    "error_code": 401,
    "error_message": "Contraseña incorrecta",
    "intentos_restantes": 2,
    "sugerencia": "Verifique que la tecla Mayúsculas no esté activada."
  }
}
```

## 🔧 Notas Técnicas

### 🚀 Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| `POST` | `/api/v1/auth/login` | Autentica usuario y genera token JWT |
| `POST` | `/api/v1/auth/logout` | Cierra sesión e invalida el token activo |
| `GET` | `/api/v1/auth/me` | Retorna datos del usuario autenticado |
| `GET` | `/api/v1/auth/validar` | Valida que el token JWT sea vigente |

### 📤 Ejemplo de Respuesta JSON

```json
{
  "success": true,
  "statusCode": 200,
  "message": "Inicio de sesión exitoso",
  "data": {
    "token": "eyJhbGciOiJI",
    "tipo_token": "Bearer",
    "usuario": {
      "id": 1,
      "nombre": "Erick Gutierrez",
      "correo": "erick@gmail.com",
      "rol": "ESTUDIANTE"
    }
  }
}
```

## 🧪 Requisitos de Pruebas

## 🔍 Casos de Prueba Funcional

### ✅ Caso 1: Login exitoso

- **Precondición:** El usuario existe en el sistema y su cuenta está activa.
- **Acción:** Ejecutar POST /api/v1/auth/login con correo y contraseña correctos.
- **Resultado esperado:**
  - Código HTTP 200 OK
  - Campo success igual a true
  - Campo token presente y no vacío
  - Campo rol con el valor correspondiente al usuario

### ✅ Caso 2: Logout exitoso

- **Precondición:** :  El usuario tiene una sesión activa con token válido.
- **Acción:** Ejecutar POST /api/v1/auth/logout con el token en el header.

- **Resultado esperado:**
  - Código HTTP 200 OK
  - El token queda invalidado para peticiones posteriores

### ❌ Caso 3: Credenciales incorrectas

- **Precondición:**  El usuario existe pero ingresa una contraseña incorrecta.
- **Acción:** Ejecutar POST /api/v1/auth/login con contraseña errónea.
- **Resultado esperado:**
  - Código HTTP 401 Unauthorized
  - Campo error_message con texto descriptivo
  - Campo intentos_restantes decrementado

### ❌ Caso 4: Cuenta bloqueada

- **Precondición:**  El usuario ha fallado 5 intentos consecutivos de login.
- **Acción:** Ejecutar POST /api/v1/auth/login
- **Resultado esperado:**
  - Código HTTP 403 Forbidden
  - Campo message indica que la cuenta está bloqueada temporalmente

### ❌ Caso 5: Token inválido o expirado

- **Precondición:**  El usuario envía una petición con un token vencido o manipulado
- **Acción:** Ejecutar GET /api/v1/auth/validar con token inválido.
- **Resultado esperado:**
  - Código HTTP 401 Unauthorized
  - Campo message indica que el token no es válido

## ✅ Definición de Hecho

## 📦 Alcance Funcional
- [ ] El endpoint de login autentica correctamente y retorna token JWT.
- [ ] El logout invalida el token activo.
- [ ] El bloqueo por intentos fallidos funciona correctamente.
- [ ] La respuesta JSON cumple con el contrato definido.

  ## 🧪 Pruebas Completadas

- [ ] Se ejecutaron pruebas unitarias para validación de credenciales.
- [ ] Se cubrieron los casos de error, cuenta bloqueada y token expirado.
- [ ] Las pruebas funcionales están documentadas y pasadas.

  ## 📄 Documentación Técnica

- [ ] Endpoints documentado en Swagger / OpenAPI.
- [ ] Se describe:

  - Propósito del endpoint
  - Campos de entrada y salida
  - Ejemplo de respuesta exitosa
  - Ejemplo de error

  ## 🔐 Manejo de Errores

- [ ] Se retorna HTTP 401 para credenciales incorrectas o token inválido.
- [ ] El campo `mensaje` incluye texto claro y amigable en todos los casos de error.
- [ ] Se retorna HTTP 403 cuando la cuenta está bloqueada.