** Validación de permisos y niveles de acceso por rol

** Historia de usuario:

**Como** sistema de autorización (middleware/guardia de rutas)

**Quiero** verificar el rol y los permisos contenidos en el token JWT antes de permitir el acceso a cada recurso o endpoint

**Para** poder asegurar que cada usuario solo acceda a las funcionalidades correspondientes a su rol (administrador, operador, consultor, etc.)