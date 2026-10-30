from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)


class LoginVista(QWidget):
    """
    Clase: LoginVista
    Descripción: Es la ventana de inicio de sesión. Solo muestra los campos
    y el botón, y le pasa al controlador lo que el usuario escribió.
    No toma decisiones por sí sola.
    """

    def __init__(self):
        super().__init__()
        self.__controlador = None

        self.setWindowTitle("Inicio de sesión")
        self.setMinimumWidth(340)

        titulo = QLabel("Barbería y Peluquería")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setStyleSheet("font-size: 20px; font-weight: bold;")

        self.__campo_usuario = QLineEdit()
        self.__campo_usuario.setPlaceholderText("Nombre de usuario")

        self.__campo_contrasena = QLineEdit()
        self.__campo_contrasena.setPlaceholderText("Contraseña")
        self.__campo_contrasena.setEchoMode(QLineEdit.EchoMode.Password)

        self.__etiqueta_error = QLabel("")
        self.__etiqueta_error.setStyleSheet("color: #C62828;")
        self.__etiqueta_error.setWordWrap(True)

        self.__boton_ingresar = QPushButton("Ingresar")

        diseno = QVBoxLayout()
        diseno.setContentsMargins(30, 30, 30, 30)
        diseno.setSpacing(12)
        diseno.addWidget(titulo)
        diseno.addWidget(self.__campo_usuario)
        diseno.addWidget(self.__campo_contrasena)
        diseno.addWidget(self.__etiqueta_error)
        diseno.addWidget(self.__boton_ingresar)
        self.setLayout(diseno)

        self.setStyleSheet("""
            QWidget {
                background-color: #F4F6F8; color: #1B2733; font-size: 14px;
            }
            QLineEdit {
                padding: 8px; border: 1px solid #B0BAC5;
                border-radius: 6px; background: white; color: #1B2733;
                placeholder-text-color: #7A8896;
            }
            QLineEdit:focus { border: 1px solid #1F6FEB; }
            QPushButton {
                padding: 10px; background-color: #1F6FEB; color: white;
                border: none; border-radius: 6px; font-weight: bold;
            }
            QPushButton:hover { background-color: #1A5FCC; }
        """)

        self.__boton_ingresar.clicked.connect(self.__al_presionar_ingresar)
        self.__campo_contrasena.returnPressed.connect(self.__al_presionar_ingresar)

    def asignar_controlador(self, controlador):
        self.__controlador = controlador

    def __al_presionar_ingresar(self):
        self.__etiqueta_error.setText("")
        nombre_usuario = self.__campo_usuario.text()
        contrasena = self.__campo_contrasena.text()
        self.__controlador.iniciar_sesion(nombre_usuario, contrasena)

    def mostrar_error(self, mensaje):
        self.__etiqueta_error.setText(mensaje)

    def abrir_pantalla_principal(self):
        self.__campo_contrasena.clear()
        QMessageBox.information(
            self, "Inicio de sesión", "Inicio de sesión correcto."
        )