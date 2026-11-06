LIMITE_RESULTADOS = 50


class ListaClientesControlador:
    """
    Clase: ListaClientesControlador
    Descripción: Le pide al modelo los clientes (los más recientes o los que
    coinciden con la búsqueda) y le dice a la vista qué mostrar.
    """

    def __init__(self, vista, modelo):
        self.vista = vista
        self.modelo = modelo

    def mostrar_recientes(self):
        self.buscar("")

    def buscar(self, texto):
        texto = texto.strip()
        try:
            clientes = self.modelo.listar_clientes(texto, LIMITE_RESULTADOS)
        except ConnectionError:
            self.vista.mostrar_clientes([])
            self.vista.mostrar_estado(
                "No se pudo conectar con la base de datos. Verifique que MySQL esté encendido."
            )
            return

        self.vista.mostrar_clientes(clientes)
        self.vista.mostrar_estado(self.__texto_estado(texto, len(clientes)))

    def volver(self):
        self.vista.volver_a_gestion()

    def __texto_estado(self, texto, cantidad):
        """
        Arma el mensaje que aparece encima de la tabla.
        """
        if texto == "":
            if cantidad == 0:
                return "Aún no hay clientes registrados."
            if cantidad == 1:
                return "Mostrando el cliente registrado."
            return "Mostrando los " + str(cantidad) + " clientes registrados más recientemente."

        if cantidad == 0:
            return "No se encontraron clientes para «" + texto + "»."
        if cantidad == 1:
            return "1 cliente encontrado para «" + texto + "»."
        if cantidad == LIMITE_RESULTADOS:
            return (
                "Mostrando los primeros " + str(cantidad) + " resultados para «" + texto
                + "». Escriba más letras para afinar la búsqueda."
            )
        return str(cantidad) + " clientes encontrados para «" + texto + "»."