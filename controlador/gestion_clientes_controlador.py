ROLES_PERMITIDOS = ["administrador", "barbero", "peluquero"]


class GestionClientesControlador:
    """
    Clase: GestionClientesControlador
    Descripción: Atiende los clics de la pantalla Gestión de clientes.
    Antes de abrir el formulario de registro revisa que haya una sesión
    iniciada y que el rol de quien la inició tenga permiso.
    """

    def __init__(self, vista, sesion):
        self.vista = vista
        self.sesion = sesion

    def abrir_registro_cliente(self):
        if not self.sesion.hay_sesion_iniciada():
            self.vista.solicitar_inicio_sesion()
            return

        if self.sesion.obtener_rol() not in ROLES_PERMITIDOS:
            self.vista.mostrar_aviso("Acceso denegado: su rol no permite registrar clientes.")
            return

        self.vista.abrir_formulario_registro()

    def abrir_lista_clientes(self):
        if not self.sesion.hay_sesion_iniciada():
            self.vista.solicitar_inicio_sesion()
            return
        self.vista.abrir_lista()

    def volver_al_panel(self):
        self.vista.volver_al_panel()