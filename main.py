import sys
from PySide6.QtWidgets import QApplication

from modelo.verificacion_login import VerificacionLogin
from modelo.sesion import Sesion
from vista.login_vista import LoginVista
from controlador.login_controlador import LoginControlador


def main():
    app = QApplication(sys.argv)

    sesion = Sesion()
    modelo = VerificacionLogin()
    vista = LoginVista()
    controlador = LoginControlador(vista, modelo, sesion)
    vista.asignar_controlador(controlador)

    vista.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()