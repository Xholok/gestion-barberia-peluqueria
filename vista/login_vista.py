from PySide6.QtCore import Qt, QByteArray
from PySide6.QtGui import QIcon, QPixmap, QPainter
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtWidgets import (
    QWidget, QFrame, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)

SVG_AVATAR = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">'
    '<circle cx="50" cy="50" r="50" fill="#1D1730"/>'
    '<circle cx="50" cy="38" r="13" fill="none" stroke="white" stroke-width="3.5"/>'
    '<path d="M24 76 C24 62 36 56 50 56 C64 56 76 62 76 76 Z" '
    'fill="none" stroke="white" stroke-width="3.5" stroke-linejoin="round"/>'
    '</svg>'
)
SVG_USUARIO = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">'
    '<circle cx="12" cy="8" r="4.5" fill="#5B5670"/>'
    '<path d="M3.5 21 C3.5 15.5 7.5 13 12 13 C16.5 13 20.5 15.5 20.5 21 Z" fill="#5B5670"/>'
    '</svg>'
)
SVG_CANDADO = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">'
    '<rect x="4.5" y="10.5" width="15" height="11" rx="2" fill="#5B5670"/>'
    '<path d="M8 10.5 V7.5 A4 4 0 0 1 16 7.5 V10.5" fill="none" '
    'stroke="#5B5670" stroke-width="2.4"/>'
    '</svg>'
)


def crear_imagen(codigo_svg, tamano):
    """
    Convierte un dibujo SVG en una imagen del tamaño indicado.
    Se dibuja al doble de tamaño para que se vea nítida en pantallas grandes.
    """
    renderizador = QSvgRenderer(QByteArray(codigo_svg.encode("utf-8")))
    imagen = QPixmap(tamano * 2, tamano * 2)
    imagen.fill(Qt.GlobalColor.transparent)
    pintor = QPainter(imagen)
    renderizador.render(pintor)
    pintor.end()
    imagen.setDevicePixelRatio(2)
    return imagen


class LoginVista(QWidget):
    """
    Clase: LoginVista
    Descripción: Es la ventana de inicio de sesión. Solo muestra los campos
    y el botón, y le pasa al controlador lo que el usuario escribió.
    No toma decisiones por sí sola.
    """

    TAMANO_AVATAR = 96

    def __init__(self):
        super().__init__()
        self.__controlador = None

        self.setObjectName("LoginVista")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setWindowTitle("Inicio de sesión")
        self.setFixedSize(440, 580)

        # Tarjeta central donde van los campos
        self.__tarjeta = QFrame()
        self.__tarjeta.setObjectName("tarjeta")

        etiqueta_aplicacion = QLabel("BARBERÍA Y PELUQUERÍA")
        etiqueta_aplicacion.setObjectName("etiquetaAplicacion")
        etiqueta_aplicacion.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.__campo_usuario = QLineEdit()
        self.__campo_usuario.setPlaceholderText("Nombre de usuario")
        self.__campo_usuario.addAction(
            QIcon(crear_imagen(SVG_USUARIO, 18)),
            QLineEdit.ActionPosition.LeadingPosition
        )

        self.__campo_contrasena = QLineEdit()
        self.__campo_contrasena.setPlaceholderText("Contraseña")
        self.__campo_contrasena.setEchoMode(QLineEdit.EchoMode.Password)
        self.__campo_contrasena.addAction(
            QIcon(crear_imagen(SVG_CANDADO, 18)),
            QLineEdit.ActionPosition.LeadingPosition
        )

        self.__etiqueta_error = QLabel("")
        self.__etiqueta_error.setObjectName("etiquetaError")
        self.__etiqueta_error.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.__etiqueta_error.setWordWrap(True)
        self.__etiqueta_error.setMinimumHeight(36)

        self.__boton_ingresar = QPushButton("INGRESAR")
        self.__boton_ingresar.setCursor(Qt.CursorShape.PointingHandCursor)

        diseno_tarjeta = QVBoxLayout(self.__tarjeta)
        diseno_tarjeta.setContentsMargins(34, 78, 34, 34)
        diseno_tarjeta.setSpacing(14)
        diseno_tarjeta.addWidget(etiqueta_aplicacion)
        diseno_tarjeta.addSpacing(6)
        diseno_tarjeta.addWidget(self.__campo_usuario)
        diseno_tarjeta.addWidget(self.__campo_contrasena)
        diseno_tarjeta.addWidget(self.__etiqueta_error)
        diseno_tarjeta.addWidget(self.__boton_ingresar)

        diseno_ventana = QVBoxLayout(self)
        diseno_ventana.setContentsMargins(40, 40, 40, 40)
        diseno_ventana.addStretch()
        diseno_ventana.addWidget(self.__tarjeta)
        diseno_ventana.addStretch()

        self.__avatar = QLabel(self)
        self.__avatar.setPixmap(crear_imagen(SVG_AVATAR, self.TAMANO_AVATAR))
        self.__avatar.setFixedSize(self.TAMANO_AVATAR, self.TAMANO_AVATAR)
        self.__avatar.setStyleSheet("background: transparent;")

        self.__aplicar_estilo()

        self.__boton_ingresar.clicked.connect(self.__al_presionar_ingresar)
        self.__campo_contrasena.returnPressed.connect(self.__al_presionar_ingresar)
        self.__campo_usuario.returnPressed.connect(self.__campo_contrasena.setFocus)

    def __aplicar_estilo(self):
        self.setStyleSheet("""
            #LoginVista {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 #2A2237, stop:1 #4B3D68);
            }
            #tarjeta {
                background-color: rgba(122, 100, 168, 140);
                border: 1px solid rgba(255, 255, 255, 40);
                border-radius: 6px;
            }
            #etiquetaAplicacion {
                background: transparent; color: #E6DEF5;
                font-size: 13px; font-weight: bold;
            }
            #etiquetaError {
                background: transparent; color: #FFC2C2; font-size: 13px;
            }
            #tarjeta QLineEdit {
                background-color: white; color: #1B1730;
                border: 2px solid transparent; border-radius: 3px;
                padding: 10px 8px; font-size: 14px;
                placeholder-text-color: #8A859C;
            }
            #tarjeta QLineEdit:focus { border: 2px solid #CDBBF2; }
            #tarjeta QPushButton {
                background-color: #1C1530; color: white; border: none;
                border-radius: 3px; padding: 14px;
                font-size: 14px; font-weight: bold;
            }
            #tarjeta QPushButton:hover { background-color: #2D2349; }
            #tarjeta QPushButton:pressed { background-color: #140F24; }
        """)

    def __colocar_avatar(self):
        x = (self.width() - self.TAMANO_AVATAR) // 2
        y = self.__tarjeta.geometry().top() - self.TAMANO_AVATAR // 2
        self.__avatar.move(x, y)
        self.__avatar.raise_()

    def showEvent(self, evento):
        super().showEvent(evento)
        self.__colocar_avatar()

    def resizeEvent(self, evento):
        super().resizeEvent(evento)
        self.__colocar_avatar()

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