import sys
from PySide6.QtWidgets import QApplication

from modelo.verificacion_login import VerificacionLogin
from modelo.sesion import Sesion
from vista.login_vista import LoginVista
from vista.panel_principal_vista import PanelPrincipalVista
from controlador.login_controlador import LoginControlador
from controlador.panel_principal_controlador import PanelPrincipalControlador


def main():
    app = QApplication(sys.argv)

    sesion = Sesion()
    ventanas = {}

    def abrir_panel_principal():
        vista_panel = PanelPrincipalVista()
        controlador_panel = PanelPrincipalControlador(vista_panel, sesion)
        vista_panel.asignar_controlador(controlador_panel)
        controlador_panel.mostrar_panel()

        ventanas["panel"] = vista_panel
        ventanas["controlador_panel"] = controlador_panel

        vista_panel.show()
        ventanas["login"].close()

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