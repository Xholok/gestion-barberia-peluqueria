from datetime import date

DIAS_SEMANA = [
    "lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"
]
MESES = [
    "enero", "febrero", "marzo", "abril", "mayo", "junio",
    "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
]


class PanelPrincipalControlador:
    """
    Clase: PanelPrincipalControlador
    Descripción: Le entrega a la ventana del panel principal los datos de quien
    inició sesión y la fecha de hoy, y atiende los clics en los módulos.
    """

    def __init__(self, vista, sesion):
        self.vista = vista
        self.sesion = sesion

    def mostrar_panel(self):
        nombre = self.sesion.obtener_nombre()
        rol = self.sesion.obtener_rol()
        self.vista.mostrar_usuario(nombre, rol)
        self.vista.mostrar_fecha(self.__texto_fecha_de_hoy())

    def abrir_modulo_reservas(self):
        self.vista.mostrar_aviso("El módulo de reservas estará disponible próximamente.")

    def abrir_modulo_clientes(self):
        self.vista.mostrar_aviso("La pantalla Gestión de clientes se construye en el siguiente paso.")

    def __texto_fecha_de_hoy(self):
        hoy = date.today()
        dia_semana = DIAS_SEMANA[hoy.weekday()].capitalize()
        mes = MESES[hoy.month - 1]
        return dia_semana + ", " + str(hoy.day) + " de " + mes + " de " + str(hoy.year)