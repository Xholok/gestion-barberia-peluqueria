class GestionClientesControlador:
    """
    Clase: GestionClientesControlador
    Descripción: Atiende los clics de la pantalla Gestión de clientes:
    abrir el registro de un cliente y volver al panel principal.
    """

    def __init__(self, vista):
        self.vista = vista

    def abrir_registro_cliente(self):
        self.vista.mostrar_aviso("El formulario de registro de cliente se construye en el siguiente paso.")

    def volver_al_panel(self):
        self.vista.volver_al_panel()