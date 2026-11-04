from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget, QFrame, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPlainTextEdit,
    QRadioButton, QButtonGroup, QCheckBox, QPushButton, QScrollArea, QMessageBox
)

LARGO_MAXIMO_OBSERVACIONES = 200

TEXTO_AUTORIZACION = (
    "Los datos del cliente se usarán únicamente para confirmar y avisar sus turnos. "
    "El cliente puede consultarlos, actualizarlos y pedir su eliminación en cualquier "
    "momento (Ley 1581 de 2012). Marque la casilla solo si el cliente lo autoriza de "
    "forma expresa."
)


class RegistroClienteVista(QWidget):
    """
    Clase: RegistroClienteVista
    Descripción: Es el formulario para registrar un cliente nuevo. Muestra los
    campos, los mensajes de error y la autorización de datos, y le pasa al
    controlador lo que se escribió. No decide si los datos están bien.
    """

    volver_solicitado = Signal()

    def __init__(self):
        super().__init__()
        self.__controlador = None

        self.setObjectName("RegistroCliente")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setWindowTitle("Registrar cliente")
        self.resize(1020, 640)
        self.setMinimumWidth(900)

        boton_volver = QPushButton("←  Volver a Gestión de clientes")
        boton_volver.setObjectName("botonVolver")
        boton_volver.setCursor(Qt.CursorShape.PointingHandCursor)

        barra_superior = QHBoxLayout()
        barra_superior.addWidget(boton_volver)
        barra_superior.addStretch()

        titulo = QLabel("Registrar cliente")
        titulo.setObjectName("tituloPantalla")
        subtitulo = QLabel("Los campos marcados con * son obligatorios.")
        subtitulo.setObjectName("subtituloPantalla")

        self.__campo_nombre = QLineEdit()
        self.__campo_nombre.setPlaceholderText("Nombre completo del cliente")
        self.__campo_nombre.setMaxLength(100)
        self.__error_nombre = self.__crear_etiqueta_error()

        self.__campo_telefono = QLineEdit()
        self.__campo_telefono.setPlaceholderText("10 dígitos. Ejemplo: 3001234567")
        self.__campo_telefono.setMaxLength(15)
        self.__error_telefono = self.__crear_etiqueta_error()

        self.__radio_whatsapp_si = QRadioButton("Sí")
        self.__radio_whatsapp_no = QRadioButton("No")
        self.__radio_whatsapp_si.setChecked(True)
        self.__grupo_whatsapp = QButtonGroup(self)
        self.__grupo_whatsapp.addButton(self.__radio_whatsapp_si)
        self.__grupo_whatsapp.addButton(self.__radio_whatsapp_no)

        fila_whatsapp = QHBoxLayout()
        fila_whatsapp.setSpacing(18)
        fila_whatsapp.addWidget(self.__radio_whatsapp_si)
        fila_whatsapp.addWidget(self.__radio_whatsapp_no)
        fila_whatsapp.addStretch()

        columna_izquierda = QVBoxLayout()
        columna_izquierda.setSpacing(4)
        columna_izquierda.addWidget(self.__crear_etiqueta_campo("Nombre *"))
        columna_izquierda.addWidget(self.__campo_nombre)
        columna_izquierda.addWidget(self.__error_nombre)
        columna_izquierda.addSpacing(6)
        columna_izquierda.addWidget(self.__crear_etiqueta_campo("Teléfono *"))
        columna_izquierda.addWidget(self.__campo_telefono)
        columna_izquierda.addWidget(self.__error_telefono)
        columna_izquierda.addSpacing(6)
        columna_izquierda.addWidget(self.__crear_etiqueta_campo("¿Usa WhatsApp en este número? *"))
        columna_izquierda.addLayout(fila_whatsapp)
        columna_izquierda.addStretch()

        self.__campo_observaciones = QPlainTextEdit()
        self.__campo_observaciones.setPlaceholderText(
            "Preferencias o detalles útiles para atender al cliente (opcional)"
        )
        self.__error_observaciones = self.__crear_etiqueta_error()

        aviso_observaciones = QLabel("No escriba datos sensibles, como información de salud.")
        aviso_observaciones.setObjectName("textoAyuda")
        aviso_observaciones.setWordWrap(True)

        self.__contador_observaciones = QLabel("0/" + str(LARGO_MAXIMO_OBSERVACIONES))
        self.__contador_observaciones.setObjectName("contadorObservaciones")
        self.__contador_observaciones.setProperty("excedido", False)

        pie_observaciones = QHBoxLayout()
        pie_observaciones.addWidget(aviso_observaciones, 1)
        pie_observaciones.addWidget(self.__contador_observaciones)

        columna_derecha = QVBoxLayout()
        columna_derecha.setSpacing(4)
        columna_derecha.addWidget(self.__crear_etiqueta_campo("Observaciones"))
        columna_derecha.addWidget(self.__campo_observaciones, 1)
        columna_derecha.addLayout(pie_observaciones)
        columna_derecha.addWidget(self.__error_observaciones)

        fila_campos = QHBoxLayout()
        fila_campos.setSpacing(28)
        fila_campos.addLayout(columna_izquierda, 1)
        fila_campos.addLayout(columna_derecha, 1)

        titulo_autorizacion = QLabel("Autorización de tratamiento de datos personales")
        titulo_autorizacion.setObjectName("tituloAutorizacion")

        texto_autorizacion = QLabel(TEXTO_AUTORIZACION)
        texto_autorizacion.setObjectName("textoAutorizacion")
        texto_autorizacion.setWordWrap(True)

        self.__casilla_autorizacion = QCheckBox(
            "El cliente autoriza el tratamiento de sus datos personales *"
        )
        self.__error_autorizacion = self.__crear_etiqueta_error()

        bloque_autorizacion = QFrame()
        bloque_autorizacion.setObjectName("bloqueAutorizacion")
        diseno_autorizacion = QVBoxLayout(bloque_autorizacion)
        diseno_autorizacion.setContentsMargins(16, 12, 16, 12)
        diseno_autorizacion.setSpacing(6)
        diseno_autorizacion.addWidget(titulo_autorizacion)
        diseno_autorizacion.addWidget(texto_autorizacion)
        diseno_autorizacion.addWidget(self.__casilla_autorizacion)
        diseno_autorizacion.addWidget(self.__error_autorizacion)

        tarjeta = QFrame()
        tarjeta.setObjectName("tarjetaFormulario")
        diseno_tarjeta = QVBoxLayout(tarjeta)
        diseno_tarjeta.setContentsMargins(22, 20, 22, 20)
        diseno_tarjeta.setSpacing(14)
        diseno_tarjeta.addLayout(fila_campos)
        diseno_tarjeta.addWidget(bloque_autorizacion)

        contenedor = QWidget()
        contenedor.setFixedWidth(820)
        diseno_contenedor = QVBoxLayout(contenedor)
        diseno_contenedor.setContentsMargins(0, 0, 0, 0)
        diseno_contenedor.setSpacing(4)
        diseno_contenedor.addWidget(titulo)
        diseno_contenedor.addWidget(subtitulo)
        diseno_contenedor.addSpacing(12)
        diseno_contenedor.addWidget(tarjeta)

        fila_centrada = QHBoxLayout()
        fila_centrada.addStretch()
        fila_centrada.addWidget(contenedor)
        fila_centrada.addStretch()

        contenido = QWidget()
        contenido.setObjectName("contenidoFormulario")
        diseno_contenido = QVBoxLayout(contenido)
        diseno_contenido.setContentsMargins(0, 0, 10, 0)
        diseno_contenido.addLayout(fila_centrada)
        diseno_contenido.addStretch()

        zona_desplazable = QScrollArea()
        zona_desplazable.setObjectName("zonaDesplazable")
        zona_desplazable.setWidgetResizable(True)
        zona_desplazable.setFrameShape(QFrame.Shape.NoFrame)
        zona_desplazable.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        zona_desplazable.setWidget(contenido)
        zona_desplazable.viewport().setObjectName("visorFormulario")

        self.__error_general = self.__crear_etiqueta_error()
        self.__error_general.setAlignment(Qt.AlignmentFlag.AlignRight)

        boton_cancelar = QPushButton("Cancelar")
        boton_cancelar.setObjectName("botonCancelar")
        boton_cancelar.setCursor(Qt.CursorShape.PointingHandCursor)

        boton_registrar = QPushButton("Registrar cliente")
        boton_registrar.setObjectName("botonRegistrar")
        boton_registrar.setCursor(Qt.CursorShape.PointingHandCursor)

        fila_botones = QHBoxLayout()
        fila_botones.setSpacing(12)
        fila_botones.addWidget(self.__error_general, 1)
        fila_botones.addWidget(boton_cancelar)
        fila_botones.addWidget(boton_registrar)

        contenedor_botones = QWidget()
        contenedor_botones.setFixedWidth(820)
        diseno_botones = QVBoxLayout(contenedor_botones)
        diseno_botones.setContentsMargins(0, 0, 0, 0)
        diseno_botones.addLayout(fila_botones)

        fila_botones_centrada = QHBoxLayout()
        fila_botones_centrada.addStretch()
        fila_botones_centrada.addWidget(contenedor_botones)
        fila_botones_centrada.addStretch()

        diseno = QVBoxLayout(self)
        diseno.setContentsMargins(26, 26, 16, 22)
        diseno.setSpacing(8)
        diseno.addLayout(barra_superior)
        diseno.addWidget(zona_desplazable, 1)
        diseno.addLayout(fila_botones_centrada)

        self.__aplicar_estilo()

        boton_volver.clicked.connect(self.__al_presionar_cancelar)
        boton_cancelar.clicked.connect(self.__al_presionar_cancelar)
        boton_registrar.clicked.connect(self.__al_presionar_registrar)
        self.__campo_nombre.returnPressed.connect(self.__campo_telefono.setFocus)
        self.__campo_observaciones.textChanged.connect(self.__al_cambiar_observaciones)

    def __crear_etiqueta_campo(self, texto):
        etiqueta = QLabel(texto)
        etiqueta.setObjectName("etiquetaCampo")
        return etiqueta

    def __crear_etiqueta_error(self):
        etiqueta = QLabel("")
        etiqueta.setObjectName("textoError")
        etiqueta.setTextFormat(Qt.TextFormat.PlainText)
        etiqueta.setWordWrap(True)
        etiqueta.setVisible(False)
        return etiqueta

    def __aplicar_estilo(self):
        self.setStyleSheet("""
            #RegistroCliente {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 #1E2A32, stop:1 #31414D);
            }
            #zonaDesplazable { background: transparent; border: none; }
            #visorFormulario { background: transparent; }
            #contenidoFormulario { background: transparent; }
            #zonaDesplazable QScrollBar:vertical {
                background: transparent; width: 10px; margin: 0;
            }
            #zonaDesplazable QScrollBar::handle:vertical {
                background: rgba(255, 255, 255, 70); border-radius: 5px; min-height: 30px;
            }
            #zonaDesplazable QScrollBar::add-line:vertical,
            #zonaDesplazable QScrollBar::sub-line:vertical { height: 0; }
            #zonaDesplazable QScrollBar::add-page:vertical,
            #zonaDesplazable QScrollBar::sub-page:vertical { background: transparent; }

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

            #tarjetaFormulario {
                background-color: rgba(255, 255, 255, 18);
                border: 1px solid rgba(255, 255, 255, 40);
                border-radius: 14px;
            }
            #etiquetaCampo {
                background: transparent; color: #E2E8F0;
                font-size: 13px; font-weight: bold;
            }
            #textoAyuda { background: transparent; color: #94A3B8; font-size: 12px; }
            #textoError { background: transparent; color: #FCA5A5; font-size: 12px; }
            #contadorObservaciones {
                background: transparent; color: #94A3B8; font-size: 12px;
            }
            #contadorObservaciones[excedido="true"] { color: #FCA5A5; font-weight: bold; }

            #tarjetaFormulario QLineEdit {
                background-color: #FFFFFF; color: #1F2937;
                border: 2px solid transparent; border-radius: 8px;
                padding: 8px 12px; font-size: 14px;
                placeholder-text-color: #9CA3AF; selection-background-color: #FDBA74;
            }
            #tarjetaFormulario QPlainTextEdit {
                background-color: #FFFFFF; color: #1F2937;
                border: 2px solid transparent; border-radius: 14px;
                padding: 10px 12px; font-size: 14px;
                selection-background-color: #FDBA74;
            }
            #tarjetaFormulario QLineEdit:focus,
            #tarjetaFormulario QPlainTextEdit:focus { border: 2px solid #FB923C; }
            #tarjetaFormulario QLineEdit[conError="true"],
            #tarjetaFormulario QPlainTextEdit[conError="true"] {
                border: 2px solid #F87171;
            }

            #tarjetaFormulario QRadioButton,
            #tarjetaFormulario QCheckBox {
                background: transparent; color: #E2E8F0; font-size: 14px; spacing: 8px;
            }
            #tarjetaFormulario QRadioButton::indicator,
            #tarjetaFormulario QCheckBox::indicator {
                width: 12px; height: 12px;
                background-color: #FFFFFF; border: 4px solid #FFFFFF;
            }
            #tarjetaFormulario QRadioButton::indicator { border-radius: 10px; }
            #tarjetaFormulario QCheckBox::indicator { border-radius: 5px; }
            #tarjetaFormulario QRadioButton::indicator:checked,
            #tarjetaFormulario QCheckBox::indicator:checked {
                background-color: #C2410C; border: 4px solid #FFFFFF;
            }

            #bloqueAutorizacion {
                background-color: rgba(15, 23, 30, 110);
                border: 1px solid rgba(255, 255, 255, 30);
                border-radius: 10px;
            }
            #tituloAutorizacion {
                background: transparent; color: #FFFFFF;
                font-size: 14px; font-weight: bold;
            }
            #textoAutorizacion {
                background: transparent; color: #CBD5E1; font-size: 12px;
            }

            #botonRegistrar {
                background-color: #C2410C; color: #FFFFFF; border: none;
                border-radius: 8px; padding: 11px 26px;
                font-size: 14px; font-weight: bold;
            }
            #botonRegistrar:hover { background-color: #D14E14; }
            #botonRegistrar:pressed { background-color: #A5350A; }
            #botonCancelar {
                background-color: transparent; color: #E2E8F0;
                border: 1px solid rgba(255, 255, 255, 80); border-radius: 8px;
                padding: 11px 22px; font-size: 14px;
            }
            #botonCancelar:hover { background-color: rgba(255, 255, 255, 25); }
        """)

    def asignar_controlador(self, controlador):
        self.__controlador = controlador

    def showEvent(self, evento):
        super().showEvent(evento)
        self.__campo_nombre.setFocus()

    def __al_presionar_registrar(self):
        self.__limpiar_errores()
        self.__controlador.registrar_cliente(
            self.__campo_nombre.text(),
            self.__campo_telefono.text(),
            self.__radio_whatsapp_si.isChecked(),
            self.__campo_observaciones.toPlainText(),
            self.__casilla_autorizacion.isChecked()
        )

    def __al_presionar_cancelar(self):
        self.__controlador.cancelar(self.__hay_datos())

    def __al_cambiar_observaciones(self):
        cantidad = len(self.__campo_observaciones.toPlainText())
        self.__contador_observaciones.setText(
            str(cantidad) + "/" + str(LARGO_MAXIMO_OBSERVACIONES)
        )
        excedido = cantidad > LARGO_MAXIMO_OBSERVACIONES
        self.__contador_observaciones.setProperty("excedido", excedido)
        self.__refrescar_estilo(self.__contador_observaciones)

    def __hay_datos(self):
        """
        Dice si ya se escribió o se marcó algo en el formulario.
        """
        if self.__campo_nombre.text().strip() != "":
            return True
        if self.__campo_telefono.text().strip() != "":
            return True
        if self.__campo_observaciones.toPlainText().strip() != "":
            return True
        if self.__radio_whatsapp_no.isChecked():
            return True
        return self.__casilla_autorizacion.isChecked()

    def mostrar_errores(self, errores):
        """
        Recibe un diccionario con el mensaje de cada dato incorrecto.
        Marca en rojo cada campo con error y conserva todo lo que se escribió.
        """
        self.__limpiar_errores()
        if "nombre" in errores:
            self.__poner_error(self.__error_nombre, errores["nombre"], self.__campo_nombre)
        if "telefono" in errores:
            self.__poner_error(self.__error_telefono, errores["telefono"], self.__campo_telefono)
        if "observaciones" in errores:
            self.__poner_error(
                self.__error_observaciones, errores["observaciones"], self.__campo_observaciones
            )
        if "autorizacion" in errores:
            self.__poner_error(self.__error_autorizacion, errores["autorizacion"], None)

    def mostrar_error_general(self, mensaje):
        self.__error_general.setText(mensaje)
        self.__error_general.setVisible(True)

    def mostrar_exito(self, mensaje):
        QMessageBox.information(self, "Registro de clientes", mensaje)

    def confirmar_descartar(self):
        respuesta = QMessageBox.question(
            self,
            "Descartar datos",
            "Hay datos escritos que no se han guardado.\n¿Desea descartarlos y salir?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        return respuesta == QMessageBox.StandardButton.Yes

    def limpiar_formulario(self):
        self.__limpiar_errores()
        self.__campo_nombre.clear()
        self.__campo_telefono.clear()
        self.__campo_observaciones.clear()
        self.__radio_whatsapp_si.setChecked(True)
        self.__casilla_autorizacion.setChecked(False)
        self.__campo_nombre.setFocus()

    def volver_a_gestion(self):
        self.volver_solicitado.emit()

    def __poner_error(self, etiqueta, mensaje, campo):
        etiqueta.setText(mensaje)
        etiqueta.setVisible(True)
        if campo is not None:
            campo.setProperty("conError", True)
            self.__refrescar_estilo(campo)

    def __limpiar_errores(self):
        etiquetas = [
            self.__error_nombre, self.__error_telefono, self.__error_observaciones,
            self.__error_autorizacion, self.__error_general
        ]
        for etiqueta in etiquetas:
            etiqueta.setText("")
            etiqueta.setVisible(False)

        campos = [self.__campo_nombre, self.__campo_telefono, self.__campo_observaciones]
        for campo in campos:
            campo.setProperty("conError", False)
            self.__refrescar_estilo(campo)

    def __refrescar_estilo(self, elemento):
        elemento.style().unpolish(elemento)
        elemento.style().polish(elemento)