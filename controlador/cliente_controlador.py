from modelo.cliente_modelo import TelefonoRepetidoError

LARGO_MINIMO_NOMBRE = 2
LARGO_MAXIMO_NOMBRE = 60
LARGO_TELEFONO = 10
LARGO_MAXIMO_OBSERVACIONES = 200


class ClienteControlador:
    """
    Clase: ClienteControlador
    Descripción: Recibe lo que se escribió en el formulario de registro de cliente,
    revisa que los datos estén bien y que haya una sesión iniciada, y si todo
    está correcto le pide al modelo que guarde al cliente.
    """

    def __init__(self, vista, modelo, sesion):
        self.vista = vista
        self.modelo = modelo
        self.sesion = sesion

    def registrar_cliente(self, nombre, telefono, usa_whatsapp, observaciones, autoriza_datos):
        if not self.sesion.hay_sesion_iniciada():
            self.vista.mostrar_error_general("Debe iniciar sesión para registrar clientes.")
            return

        nombre = " ".join(nombre.split())
        observaciones = observaciones.strip()

        errores = {}

        mensaje_nombre = self.__revisar_nombre(nombre)
        if mensaje_nombre != "":
            errores["nombre"] = mensaje_nombre

        mensaje_telefono = self.__revisar_telefono(telefono)
        if mensaje_telefono != "":
            errores["telefono"] = mensaje_telefono

        if len(observaciones) > LARGO_MAXIMO_OBSERVACIONES:
            errores["observaciones"] = (
                "Las observaciones no pueden pasar de "
                + str(LARGO_MAXIMO_OBSERVACIONES) + " caracteres."
            )

        if not autoriza_datos:
            errores["autorizacion"] = (
                "Debe confirmar que el cliente autoriza el tratamiento de sus datos."
            )

        if "telefono" not in errores:
            try:
                dueno = self.modelo.buscar_por_telefono(telefono)
            except ConnectionError:
                self.vista.mostrar_error_general(
                    "No se pudo conectar con la base de datos. Verifique que MySQL esté encendido."
                )
                return
            if dueno is not None and dueno["es_cliente"]:
                errores["telefono"] = (
                    "Este teléfono ya está registrado a nombre de " + dueno["nombre"] + "."
                )

        if len(errores) > 0:
            self.vista.mostrar_errores(errores)
            return

        if observaciones == "":
            observaciones = None

        try:
            resultado = self.modelo.guardar_cliente(
                nombre, telefono, usa_whatsapp, observaciones,
                autoriza_datos, self.sesion.obtener_id()
            )
        except TelefonoRepetidoError:
            self.vista.mostrar_errores(
                {"telefono": "Este teléfono ya está registrado a otro cliente."}
            )
            return
        except ConnectionError:
            self.vista.mostrar_error_general(
                "No se pudo guardar el cliente. Verifique que MySQL esté encendido."
            )
            return

        fecha_texto = resultado["fecha_registro"].strftime("%d/%m/%Y %H:%M")
        resumen = (
            "Cliente registrado\n\n"
            + "Código: " + resultado["codigo"] + "\n"
            + "Nombre: " + resultado["nombre"] + "\n"
            + "Fecha y hora: " + fecha_texto + "\n"
            + "Registrado por: " + self.sesion.obtener_nombre() + "\n"
            + "Estado: Activo"
        )
        if resultado["vinculado_a_usuario"]:
            resumen = resumen + (
                "\n\nEste teléfono pertenece a un usuario del sistema; "
                "se registró como cliente con los datos que ya tenía."
            )
        self.vista.mostrar_exito(resumen)
        self.vista.limpiar_formulario()

    def cancelar(self, hay_datos):
        if hay_datos:
            if not self.vista.confirmar_descartar():
                return
        self.vista.volver_a_gestion()

    def __revisar_nombre(self, nombre):
        """
        Devuelve el mensaje de error del nombre, o un texto vacío si está bien.
        """
        if nombre == "":
            return "El nombre es obligatorio."
        if len(nombre) < LARGO_MINIMO_NOMBRE or len(nombre) > LARGO_MAXIMO_NOMBRE:
            return (
                "El nombre debe tener entre " + str(LARGO_MINIMO_NOMBRE)
                + " y " + str(LARGO_MAXIMO_NOMBRE) + " caracteres."
            )
        for caracter in nombre:
            if not caracter.isalpha() and caracter != " ":
                return "El nombre solo puede tener letras y espacios."
        return ""

    def __revisar_telefono(self, telefono):
        """
        Devuelve el mensaje de error del teléfono, o un texto vacío si está bien.
        """
        if telefono == "":
            return "El teléfono es obligatorio."
        solo_numeros = True
        for caracter in telefono:
            if caracter not in "0123456789":
                solo_numeros = False
        if not solo_numeros or len(telefono) != LARGO_TELEFONO:
            return "El teléfono debe tener exactamente 10 dígitos, solo números."
        if telefono[0] != "3":
            return "El teléfono debe empezar por 3."
        return ""