import sys
from PySide6.QtWidgets import QApplication

from modelo.verificacion_login import VerificacionLogin
from modelo.cliente_modelo import ClienteModelo
from modelo.sesion import Sesion
from vista.login_vista import LoginVista
from vista.panel_principal_vista import PanelPrincipalVista
from vista.gestion_clientes_vista import GestionClientesVista
from vista.registro_cliente_vista import RegistroClienteVista
from controlador.login_controlador import LoginControlador
from controlador.panel_principal_controlador import PanelPrincipalControlador
from controlador.gestion_clientes_controlador import GestionClientesControlador
from controlador.cliente_controlador import ClienteControlador


def main():
    app = QApplication(sys.argv)
    sesion = Sesion()
    ventanas = {}

    def abrir_panel_principal():
        vista_panel = PanelPrincipalVista()
        controlador_panel = PanelPrincipalControlador(vista_panel, sesion)
        vista_panel.asignar_controlador(controlador_panel)
        vista_panel.gestion_clientes_solicitada.connect(abrir_gestion_clientes)
        controlador_panel.mostrar_panel()

        ventanas["panel"] = vista_panel
        ventanas["controlador_panel"] = controlador_panel

        vista_panel.show()
        ventanas["login"].close()

    def abrir_gestion_clientes():
        vista_gestion = GestionClientesVista()
        controlador_gestion = GestionClientesControlador(vista_gestion, sesion)
        vista_gestion.asignar_controlador(controlador_gestion)
        vista_gestion.volver_solicitado.connect(volver_al_panel)
        vista_gestion.registro_cliente_solicitado.connect(abrir_registro_cliente)
        vista_gestion.inicio_sesion_solicitado.connect(pedir_inicio_sesion)

        ventanas["gestion_clientes"] = vista_gestion
        ventanas["controlador_gestion_clientes"] = controlador_gestion

        vista_gestion.setGeometry(ventanas["panel"].geometry())
        vista_gestion.show()
        ventanas["panel"].hide()

    def volver_al_panel():
        ventanas["panel"].setGeometry(ventanas["gestion_clientes"].geometry())
        ventanas["panel"].show()
        ventanas["gestion_clientes"].close()

    def abrir_registro_cliente():
        vista_registro = RegistroClienteVista()
        modelo_cliente = ClienteModelo()
        controlador_cliente = ClienteControlador(vista_registro, modelo_cliente, sesion)
        vista_registro.asignar_controlador(controlador_cliente)
        vista_registro.volver_solicitado.connect(volver_a_gestion_clientes)

        ventanas["registro_cliente"] = vista_registro
        ventanas["controlador_cliente"] = controlador_cliente

        vista_registro.setGeometry(ventanas["gestion_clientes"].geometry())
        vista_registro.show()
        ventanas["gestion_clientes"].hide()

    def volver_a_gestion_clientes():
        ventanas["gestion_clientes"].setGeometry(ventanas["registro_cliente"].geometry())
        ventanas["gestion_clientes"].show()
        ventanas["registro_cliente"].close()

    def pedir_inicio_sesion():
        ventanas["login"].show()
        ventanas["gestion_clientes"].close()
        ventanas["panel"].close()

    vista_login = LoginVista()
    modelo = VerificacionLogin()
    controlador_login = LoginControlador(vista_login, modelo, sesion)
    vista_login.asignar_controlador(controlador_login)
    vista_login.ingreso_exitoso.connect(abrir_panel_principal)

    ventanas["login"] = vista_login
    ventanas["controlador_login"] = controlador_login

    vista_login.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()