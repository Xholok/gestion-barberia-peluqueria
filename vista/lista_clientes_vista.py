from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QWidget, QFrame, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView
)

from vista.login_vista import crear_imagen

SVG_LUPA = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" '
    'stroke="#6B7280" stroke-width="2" stroke-linecap="round">'
    '<circle cx="10.5" cy="10.5" r="6"/><path d="M15 15 L20.5 20.5"/>'
    '</svg>'
)

ESPERA_BUSQUEDA = 300


class ListaClientesVista(QWidget):
    """
    Clase: ListaClientesVista
    Descripción: Muestra los clientes registrados más recientemente y permite
    buscarlos por nombre o teléfono. Solo muestra datos: la búsqueda la hace
    el controlador.
    """

    volver_solicitado = Signal()

    def __init__(self):
        super().__init__()
        self.__controlador = None

        self.setObjectName("ListaClientes")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setWindowTitle("Lista de clientes")
        self.resize(1020, 640)
        self.setMinimumSize(900, 560)

        boton_volver = QPushButton("←  Volver a Gestión de clientes")
        boton_volver.setObjectName("botonVolver")
        boton_volver.setCursor(Qt.CursorShape.PointingHandCursor)

        barra_superior = QHBoxLayout()
        barra_superior.addWidget(boton_volver)
        barra_superior.addStretch()

        titulo = QLabel("Clientes")
        titulo.setObjectName("tituloPantalla")
        subtitulo = QLabel("Busque un cliente por nombre, apellido o teléfono.")
        subtitulo.setObjectName("subtituloPantalla")

        self.__campo_busqueda = QLineEdit()
        self.__campo_busqueda.setObjectName("campoBusqueda")
        self.__campo_busqueda.setPlaceholderText("Escriba un nombre o un teléfono")
        self.__campo_busqueda.setClearButtonEnabled(True)
        self.__campo_busqueda.setMaxLength(60)
        self.__campo_busqueda.addAction(
            QIcon(crear_imagen(SVG_LUPA, 18)), QLineEdit.ActionPosition.LeadingPosition
        )

        self.__etiqueta_estado = QLabel("")
        self.__etiqueta_estado.setObjectName("etiquetaEstado")
        self.__etiqueta_estado.setTextFormat(Qt.TextFormat.PlainText)
        self.__etiqueta_estado.setWordWrap(True)

        self.__tabla = QTableWidget(0, 2)
        self.__tabla.setObjectName("tablaClientes")
        self.__tabla.setHorizontalHeaderLabels(["Nombre", "Teléfono"])
        self.__tabla.verticalHeader().setVisible(False)
        self.__tabla.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.__tabla.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.__tabla.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.__tabla.setShowGrid(False)
        self.__tabla.setAlternatingRowColors(True)
        self.__tabla.setWordWrap(False)
        self.__tabla.verticalHeader().setDefaultSectionSize(40)
        encabezado = self.__tabla.horizontalHeader()
        encabezado.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        encabezado.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        encabezado.resizeSection(1, 170)
        encabezado.setDefaultAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        encabezado.setHighlightSections(False)

        tarjeta = QFrame()
        tarjeta.setObjectName("tarjetaLista")
        diseno_tarjeta = QVBoxLayout(tarjeta)
        diseno_tarjeta.setContentsMargins(20, 20, 20, 20)
        diseno_tarjeta.setSpacing(10)
        diseno_tarjeta.addWidget(self.__campo_busqueda)
        diseno_tarjeta.addWidget(self.__etiqueta_estado)
        diseno_tarjeta.addWidget(self.__tabla, 1)

        contenedor = QWidget()
        contenedor.setObjectName("contenedorLista")
        contenedor.setMaximumWidth(760)
        diseno_contenedor = QVBoxLayout(contenedor)
        diseno_contenedor.setContentsMargins(0, 0, 0, 0)
        diseno_contenedor.setSpacing(4)
        diseno_contenedor.addWidget(titulo)
        diseno_contenedor.addWidget(subtitulo)
        diseno_contenedor.addSpacing(12)
        diseno_contenedor.addWidget(tarjeta, 1)

        fila_centrada = QHBoxLayout()
        fila_centrada.addStretch()
        fila_centrada.addWidget(contenedor, 10)
        fila_centrada.addStretch()

        diseno = QVBoxLayout(self)
        diseno.setContentsMargins(26, 26, 26, 26)
        diseno.setSpacing(10)
        diseno.addLayout(barra_superior)
        diseno.addLayout(fila_centrada, 1)

        self.__aplicar_estilo()

        self.__temporizador = QTimer(self)
        self.__temporizador.setSingleShot(True)
        self.__temporizador.setInterval(ESPERA_BUSQUEDA)
        self.__temporizador.timeout.connect(self.__buscar_ahora)

        self.__campo_busqueda.textChanged.connect(self.__al_cambiar_busqueda)
        self.__campo_busqueda.returnPressed.connect(self.__buscar_ahora)
        boton_volver.clicked.connect(self.__al_presionar_volver)

    def __aplicar_estilo(self):
        self.setStyleSheet("""
            #ListaClientes {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 #1E2A32, stop:1 #31414D);
            }
            #contenedorLista { background: transparent; }
            #botonVolver {
                background: transparent; color: #CBD5E1; border: none;
                font-size: 14px; padding: 8px 4px;
            }
            #botonVolver:hover { color: #FFFFFF; }
            #tituloPantalla {
                background: transparent; color: #FFFFFF;
                font-size: 28px; font-weight: bold;
            }
            #subtituloPantalla { background: transparent; color: #CBD5E1; font-size: 14px; }

            #tarjetaLista {
                background-color: rgba(255, 255, 255, 18);
                border: 1px solid rgba(255, 255, 255, 40);
                border-radius: 14px;
            }
            #campoBusqueda {
                background-color: #FFFFFF; color: #1F2937;
                border: 2px solid transparent; border-radius: 10px;
                padding: 9px 10px; font-size: 14px;
                placeholder-text-color: #9CA3AF; selection-background-color: #FDBA74;
            }
            #campoBusqueda:focus { border: 2px solid #FB923C; }
            #etiquetaEstado { background: transparent; color: #CBD5E1; font-size: 12px; }

            #tablaClientes {
                background-color: rgba(15, 23, 30, 90);
                alternate-background-color: rgba(255, 255, 255, 12);
                color: #F1F5F9; border: none; border-radius: 10px;
                font-size: 14px;
            }
            #tablaClientes::item { padding: 0 12px; border: none; }
            #tablaClientes QHeaderView::section {
                background-color: rgba(15, 23, 30, 160); color: #FDBA74;
                border: none; padding: 8px 12px;
                font-size: 13px; font-weight: bold;
            }
            #tablaClientes QTableCornerButton::section { background: transparent; border: none; }
            #tablaClientes QScrollBar:vertical {
                background: transparent; width: 10px; margin: 2px;
            }
            #tablaClientes QScrollBar::handle:vertical {
                background: rgba(255, 255, 255, 70); border-radius: 4px; min-height: 30px;
            }
            #tablaClientes QScrollBar::add-line:vertical,
            #tablaClientes QScrollBar::sub-line:vertical { height: 0; }
            #tablaClientes QScrollBar::add-page:vertical,
            #tablaClientes QScrollBar::sub-page:vertical { background: transparent; }
        """)

    def asignar_controlador(self, controlador):
        self.__controlador = controlador

    def showEvent(self, evento):
        super().showEvent(evento)
        self.__campo_busqueda.setFocus()

    def __al_cambiar_busqueda(self):
        self.__temporizador.start()

    def __buscar_ahora(self):
        self.__temporizador.stop()
        self.__controlador.buscar(self.__campo_busqueda.text())

    def __al_presionar_volver(self):
        self.__controlador.volver()

    def mostrar_clientes(self, clientes):
        self.__tabla.setRowCount(0)
        for cliente in clientes:
            fila = self.__tabla.rowCount()
            self.__tabla.insertRow(fila)
            self.__tabla.setItem(fila, 0, QTableWidgetItem(cliente["nombre"]))
            self.__tabla.setItem(fila, 1, QTableWidgetItem(self.__formatear_telefono(cliente["telefono"])))
        self.__tabla.scrollToTop()

    def mostrar_estado(self, mensaje):
        self.__etiqueta_estado.setText(mensaje)

    def volver_a_gestion(self):
        self.volver_solicitado.emit()

    def __formatear_telefono(self, telefono):
        if len(telefono) == 10:
            return telefono[0:3] + " " + telefono[3:6] + " " + telefono[6:10]
        return telefono