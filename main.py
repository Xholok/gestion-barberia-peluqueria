import sys
from PySide6.QtWidgets import QApplication

from modelo.verificacion_login import VerificacionLogin
from modelo.sesion import Sesion
from vista.login_vista import LoginVista
from vista.panel_principal_vista import PanelPrincipalVista
from vista.gestion_clientes_vista import GestionClientesVista
from controlador.login_controlador import LoginControlador
from controlador.panel_principal_controlador import PanelPrincipalControlador
from controlador.gestion_clientes_controlador import GestionClientesControlador


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
        controlador_gestion = GestionClientesControlador(vista_gestion)
        vista_gestion.asignar_controlador(controlador_gestion)
        vista_gestion.volver_solicitado.connect(volver_al_panel)

        ventanas["gestion_clientes"] = vista_gestion
        ventanas["controlador_gestion_clientes"] = controlador_gestion

        vista_gestion.setGeometry(ventanas["panel"].geometry())
        vista_gestion.show()
        ventanas["panel"].hide()

    def volver_al_panel():
        ventanas["panel"].setGeometry(ventanas["gestion_clientes"].geometry())
        ventanas["panel"].show()
        ventanas["gestion_clientes"].close()

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