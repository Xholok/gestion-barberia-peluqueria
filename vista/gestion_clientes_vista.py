from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QMessageBox
)

from vista.login_vista import crear_imagen

SVG_REGISTRAR = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" '
    'stroke="COLOR" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">'
    '<circle cx="9" cy="8" r="3.4"/>'
    '<path d="M2.5 20 C2.5 16.5 5.4 14.2 9 14.2 C12.6 14.2 15.5 16.5 15.5 20"/>'
    '<path d="M19 8 V14 M16 11 H22"/>'
    '</svg>'
)
SVG_ELIMINAR = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" '
    'stroke="COLOR" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">'
    '<circle cx="9" cy="8" r="3.4"/>'
    '<path d="M2.5 20 C2.5 16.5 5.4 14.2 9 14.2 C12.6 14.2 15.5 16.5 15.5 20"/>'
    '<path d="M16 11 H22"/>'
    '</svg>'
)
SVG_MODIFICAR = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" '
    'stroke="COLOR" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M4 20 L8 19 L19.5 7.5 A2.1 2.1 0 0 0 16.5 4.5 L5 16 Z"/>'
    '<path d="M14.5 6.5 L17.5 9.5"/>'
    '</svg>'
)
SVG_BUSCAR = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" '
    'stroke="COLOR" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">'
    '<circle cx="10.5" cy="10.5" r="6"/>'
    '<path d="M15 15 L20.5 20.5"/>'
    '</svg>'
)


class TarjetaOpcion(QPushButton):
    """
    Clase: TarjetaOpcion
    Descripción: Es un botón grande con un icono, un título y una descripción.
    Si no está habilitado se ve apagado y no responde a los clics.
    """

    def __init__(self, codigo_svg, titulo, descripcion, habilitada):
        super().__init__()
        self.setObjectName("tarjetaOpcion")
        self.setFixedHeight(230)
        self.setMinimumWidth(200)
        self.setEnabled(habilitada)

        if habilitada:
            color_icono = "#FFFFFF"
            nombre_titulo = "tituloOpcion"
            nombre_descripcion = "descripcionOpcion"
            self.setCursor(Qt.CursorShape.PointingHandCursor)
        else:
            color_icono = "#94A3B8"
            nombre_titulo = "tituloOpcionApagado"
            nombre_descripcion = "descripcionOpcionApagada"

        icono = QLabel()
        icono.setPixmap(crear_imagen(codigo_svg.replace("COLOR", color_icono), 56))

        etiqueta_titulo = QLabel(titulo)
        etiqueta_titulo.setObjectName(nombre_titulo)
        etiqueta_titulo.setWordWrap(True)

        etiqueta_descripcion = QLabel(descripcion)
        etiqueta_descripcion.setObjectName(nombre_descripcion)
        etiqueta_descripcion.setWordWrap(True)

        diseno = QVBoxLayout(self)
        diseno.setContentsMargins(20, 20, 20, 20)
        diseno.setSpacing(10)
        diseno.addStretch()
        for elemento in (icono, etiqueta_titulo, etiqueta_descripcion):
            elemento.setAlignment(Qt.AlignmentFlag.AlignCenter)
            elemento.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
            diseno.addWidget(elemento)
        diseno.addStretch()


class GestionClientesVista(QWidget):
    """
    Clase: GestionClientesVista
    Descripción: Es la pantalla del módulo de clientes. Muestra las opciones
    (registrar, eliminar, modificar y buscar) y un botón para volver al panel.
    Por ahora solo está habilitada la opción de registrar cliente.
    """

    volver_solicitado = Signal()

    def __init__(self):
        super().__init__()
        self.__controlador = None

        self.setObjectName("GestionClientes")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setWindowTitle("Gestión de clientes")
        self.resize(1020, 640)
        self.setMinimumSize(900, 560)

        boton_volver = QPushButton("←  Volver al panel")
        boton_volver.setObjectName("botonVolver")
        boton_volver.setCursor(Qt.CursorShape.PointingHandCursor)

        titulo = QLabel("Gestión de clientes")
        titulo.setObjectName("tituloPantalla")

        subtitulo = QLabel("Elija qué desea hacer con los clientes.")
        subtitulo.setObjectName("subtituloPantalla")

        self.__tarjeta_registrar = TarjetaOpcion(
            SVG_REGISTRAR, "Registrar cliente", "Agregar un cliente nuevo", True
        )
        self.__tarjeta_eliminar = TarjetaOpcion(
            SVG_ELIMINAR, "Eliminar cliente", "Próximamente", False
        )
        self.__tarjeta_modificar = TarjetaOpcion(
            SVG_MODIFICAR, "Modificar cliente", "Próximamente", False
        )
        self.__tarjeta_buscar = TarjetaOpcion(
            SVG_BUSCAR, "Buscar cliente / ver lista", "Próximamente", False
        )

        fila_opciones = QHBoxLayout()
        fila_opciones.setSpacing(20)
        fila_opciones.addWidget(self.__tarjeta_registrar)
        fila_opciones.addWidget(self.__tarjeta_eliminar)
        fila_opciones.addWidget(self.__tarjeta_modificar)
        fila_opciones.addWidget(self.__tarjeta_buscar)

        barra_superior = QHBoxLayout()
        barra_superior.addWidget(boton_volver)
        barra_superior.addStretch()

        diseno = QVBoxLayout(self)
        diseno.setContentsMargins(26, 26, 26, 26)
        diseno.addLayout(barra_superior)
        diseno.addStretch(1)
        diseno.addWidget(titulo)
        diseno.addWidget(subtitulo)
        diseno.addSpacing(24)
        diseno.addLayout(fila_opciones)
        diseno.addStretch(2)

        self.__aplicar_estilo()

        boton_volver.clicked.connect(self.__al_presionar_volver)
        self.__tarjeta_registrar.clicked.connect(self.__al_presionar_registrar)

    def __aplicar_estilo(self):
        self.setStyleSheet("""
            #GestionClientes {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 #1E2A32, stop:1 #31414D);
            }
            #botonVolver {
                background: transparent; color: #CBD5E1; border: none;
                font-size: 14px; padding: 8px 4px;
            }
            #botonVolver:hover { color: #FFFFFF; }
            #tituloPantalla {
                background: transparent; color: #FFFFFF;
                font-size: 28px; font-weight: bold;
            }
            #subtituloPantalla {
                background: transparent; color: #CBD5E1; font-size: 14px;
            }
            #tarjetaOpcion {
                background-color: #C2410C; border: none; border-radius: 12px;
            }
            #tarjetaOpcion:hover { background-color: #D14E14; }
            #tarjetaOpcion:pressed { background-color: #A5350A; }
            #tarjetaOpcion:disabled {
                background-color: rgba(255, 255, 255, 22);
                border: 1px solid rgba(255, 255, 255, 40);
            }
            #tituloOpcion {
                background: transparent; color: #FFFFFF;
                font-size: 18px; font-weight: bold;
            }
            #descripcionOpcion {
                background: transparent; color: #FFE8DA; font-size: 13px;
            }
            #tituloOpcionApagado {
                background: transparent; color: #94A3B8;
                font-size: 18px; font-weight: bold;
            }
            #descripcionOpcionApagada {
                background: transparent; color: #7C8A9C; font-size: 13px;
            }
        """)

    def asignar_controlador(self, controlador):
        self.__controlador = controlador

    def __al_presionar_volver(self):
        self.__controlador.volver_al_panel()

    def __al_presionar_registrar(self):
        self.__controlador.abrir_registro_cliente()

    def volver_al_panel(self):
        self.volver_solicitado.emit()

    def mostrar_aviso(self, mensaje):
        QMessageBox.information(self, "Gestión de clientes", mensaje)