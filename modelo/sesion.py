class Sesion:
    """
    Clase: Sesion
    Descripción: Guarda quién inició sesión (su id, su nombre y su rol)
    mientras el programa está abierto.
    """

    def __init__(self):
        self.__id = None
        self.__nombre = None
        self.__rol = None

    def guardar(self, id, nombre, rol):
        self.__id = id
        self.__nombre = nombre
        self.__rol = rol

    def obtener_id(self):
        return self.__id

    def obtener_nombre(self):
        return self.__nombre

    def obtener_rol(self):
        return self.__rol

    def hay_sesion_iniciada(self):
        return self.__id is not None