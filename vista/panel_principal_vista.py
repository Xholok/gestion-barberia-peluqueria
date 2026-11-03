from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget, QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QMessageBox
)

from vista.login_vista import crear_imagen, SVG_AVATAR

SVG_CALENDARIO = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" '
    'stroke="#E6DEF5" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">'
    '<rect x="3.5" y="5" width="17" height="15.5" rx="2.5"/>'
    '<path d="M3.5 10 H20.5 M8 3 V7 M16 3 V7"/>'
    '<path d="M8 14 H8.01 M12 14 H12.01 M16 14 H16.01 M8 17.5 H8.01 M12 17.5 H12.01"/>'
    '</svg>'
)
SVG_CLIENTES = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" '
    'stroke="#E6DEF5" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">'
    '<circle cx="9" cy="8" r="3.2"/>'
    '<path d="M3 19.5 C3 16.2 5.7 14 9 14 C12.3 14 15 16.2 15 19.5"/>'
    '<circle cx="17" cy="9" r="2.6"/>'
    '<path d="M16.5 14.2 C19.5 14.3 21.5 16 21.5 18.8"/>'
    '</svg>'
)


class TarjetaModulo(QPushButton):
    """
    Clase: TarjetaModulo
    Descripción: Es un botón grande con un icono, un título y una descripción.
    Se usa en el panel principal para entrar a cada módulo.
    """

    def __init__(self, codigo_svg, titulo, descripcion, nombre_objeto):
        super().__init__()
        self.setObjectName(nombre_objeto)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedHeight(240)
        self.setMinimumWidth(240)

        icono = QLabel()
        icono.setPixmap(crear_imagen(codigo_svg, 64))

        etiqueta_titulo = QLabel(titulo)
        etiqueta_titulo.setObjectName("tituloModulo")

        etiqueta_descripcion = QLabel(descripcion)
        etiqueta_descripcion.setObjectName("descripcionModulo")
        etiqueta_descripcion.setWordWrap(True)

        diseno = QVBoxLayout(self)
        diseno.setContentsMargins(24, 24, 24, 24)
        diseno.setSpacing(10)
        diseno.addStretch()
        for elemento in (icono, etiqueta_titulo, etiqueta_descripcion):
            elemento.setAlignment(Qt.AlignmentFlag.AlignCenter)
            elemento.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
            diseno.addWidget(elemento)
        diseno.addStretch()


class PanelPrincipalVista(QWidget):
    """
    Clase: PanelPrincipalVista
    Descripción: Es la ventana que se abre después de iniciar sesión.
    Muestra quién inició sesión, el espacio de los turnos del día y los
    módulos del programa. No toma decisiones: avisa al controlador de los clics.
    """
    gestion_clientes_solicitada = Signal()

    def __init__(self):
        super().__init__()
        self.__controlador = None

        self.setObjectName("PanelPrincipal")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setWindowTitle("Panel principal")
        self.resize(1020, 640)
        self.setMinimumSize(900, 560)

        avatar = QLabel()
        avatar.setPixmap(crear_imagen(SVG_AVATAR, 60))
        avatar.setFixedSize(60, 60)

        self.__etiqueta_nombre = QLabel("")
        self.__etiqueta_nombre.setObjectName("nombreUsuario")
        self.__etiqueta_nombre.setWordWrap(True)

        self.__etiqueta_rol = QLabel("")
        self.__etiqueta_rol.setObjectName("rolUsuario")

        textos_usuario = QVBoxLayout()
        textos_usuario.setSpacing(2)
        textos_usuario.addStretch()
        textos_usuario.addWidget(self.__etiqueta_nombre)
        textos_usuario.addWidget(self.__etiqueta_rol)
        textos_usuario.addStretch()

        tarjeta_usuario = QFrame()
        tarjeta_usuario.setObjectName("tarjetaUsuario")
        diseno_usuario = QHBoxLayout(tarjeta_usuario)
        diseno_usuario.setContentsMargins(16, 16, 16, 16)
        diseno_usuario.setSpacing(14)
        diseno_usuario.addWidget(avatar)
        diseno_usuario.addLayout(textos_usuario, 1)

        titulo_turnos = QLabel("Turnos del día")
        titulo_turnos.setObjectName("tituloPanel")

        self.__etiqueta_fecha = QLabel("")
        self.__etiqueta_fecha.setObjectName("fechaPanel")

        mensaje_vacio = QLabel("Aún no hay turnos registrados para hoy.")
        mensaje_vacio.setObjectName("mensajeVacio")
        mensaje_vacio.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mensaje_vacio.setWordWrap(True)

        panel_turnos = QFrame()
        panel_turnos.setObjectName("panelTurnos")
        diseno_turnos = QVBoxLayout(panel_turnos)
        diseno_turnos.setContentsMargins(20, 20, 20, 20)
        diseno_turnos.setSpacing(4)
        diseno_turnos.addWidget(titulo_turnos)
        diseno_turnos.addWidget(self.__etiqueta_fecha)
        diseno_turnos.addStretch()
        diseno_turnos.addWidget(mensaje_vacio)
        diseno_turnos.addStretch()

        columna_izquierda = QWidget()
        columna_izquierda.setFixedWidth(300)
        diseno_izquierda = QVBoxLayout(columna_izquierda)
        diseno_izquierda.setContentsMargins(0, 0, 0, 0)
        diseno_izquierda.setSpacing(18)
        diseno_izquierda.addWidget(tarjeta_usuario)
        diseno_izquierda.addWidget(panel_turnos, 1)

        titulo_principal = QLabel("¿Qué desea hacer?")
        titulo_principal.setObjectName("tituloPrincipal")

        subtitulo_principal = QLabel("Elija un módulo para comenzar.")
        subtitulo_principal.setObjectName("subtituloPrincipal")

        self.__tarjeta_reservas = TarjetaModulo(
            SVG_CALENDARIO, "Reservas", "Crear y organizar los turnos del día", "tarjetaReservas"
        )
        self.__tarjeta_clientes = TarjetaModulo(
            SVG_CLIENTES, "Clientes", "Registrar y gestionar los clientes", "tarjetaClientes"
        )

        fila_modulos = QHBoxLayout()
        fila_modulos.setSpacing(24)
        fila_modulos.addWidget(self.__tarjeta_reservas)
        fila_modulos.addWidget(self.__tarjeta_clientes)

        zona_principal = QVBoxLayout()
        zona_principal.addStretch(1)
        zona_principal.addWidget(titulo_principal)
        zona_principal.addWidget(subtitulo_principal)
        zona_principal.addSpacing(24)
        zona_principal.addLayout(fila_modulos)
        zona_principal.addStretch(2)

        diseno_ventana = QHBoxLayout(self)
        diseno_ventana.setContentsMargins(26, 26, 26, 26)
        diseno_ventana.setSpacing(30)
        diseno_ventana.addWidget(columna_izquierda)
        diseno_ventana.addLayout(zona_principal, 1)

        self.__aplicar_estilo()

        self.__tarjeta_reservas.clicked.connect(self.__al_presionar_reservas)
        self.__tarjeta_clientes.clicked.connect(self.__al_presionar_clientes)

    def __aplicar_estilo(self):
        self.setStyleSheet("""
            #PanelPrincipal {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 #1E2A32, stop:1 	#31414D);
            }
            #tarjetaUsuario, #panelTurnos {
                background-color: rgba(255, 255, 255, 28);
                border: 1px solid rgba(255, 255, 255, 40);
                border-radius: 10px;
            }
            #nombreUsuario {
                background: transparent; color: #FFFFFF;
                font-size: 15px; font-weight: bold;
            }
            #rolUsuario { background: transparent; color: #CDBBF2; font-size: 13px; }
            #tituloPanel {
                background: transparent; color: #FFFFFF;
                font-size: 16px; font-weight: bold;
            }
            #fechaPanel { background: transparent; color: #CDBBF2; font-size: 12px; }
            #mensajeVacio { background: transparent; color: #C9BEDF; font-size: 13px; }
            #tituloPrincipal {
                background: transparent; color: #FFFFFF;
                font-size: 28px; font-weight: bold;
            }
            #subtituloPrincipal {
                background: transparent; color: #CDBBF2; font-size: 14px;
            }
            #tarjetaReservas { background-color: #4D7C0F; border: none; border-radius: 12px; }
            #tarjetaReservas:hover { background-color: #5B8F12; }
            #tarjetaReservas:pressed { background-color: #3F6A0C; }
            #tarjetaClientes { background-color: #C2410C; border: none; border-radius: 12px; }
            #tarjetaClientes:hover { background-color: #D14E14; }
            #tarjetaClientes:pressed { background-color: #A5350A; }
            #tituloModulo {
                background: transparent; color: #FFFFFF;
                font-size: 20px; font-weight: bold;
            }
            #descripcionModulo {
                background: transparent; color: #E0D6F2; font-size: 13px;
            }
        """)

    def asignar_controlador(self, controlador):
        self.__controlador = controlador

    def __al_presionar_reservas(self):
        self.__controlador.abrir_modulo_reservas()

    def __al_presionar_clientes(self):
        self.__controlador.abrir_modulo_clientes()

    def mostrar_usuario(self, nombre, rol):
        self.__etiqueta_nombre.setText(nombre)
        self.__etiqueta_rol.setText(rol.capitalize())

    def mostrar_fecha(self, texto):
        self.__etiqueta_fecha.setText(texto)
    
    def abrir_gestion_clientes(self):
        self.gestion_clientes_solicitada.emit()

    def mostrar_aviso(self, mensaje):
        QMessageBox.information(self, "Panel principal", mensaje)