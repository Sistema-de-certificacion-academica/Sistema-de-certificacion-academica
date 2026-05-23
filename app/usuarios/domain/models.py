class User:
    def __init__(self, id: int, nombre: str, correo: str, password: str, rol: str, activo: bool = True):
        self.id = id
        self.nombre = nombre
        self.correo = correo
        self.password = password
        self.rol = rol
        self.activo = activo