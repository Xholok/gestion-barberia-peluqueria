class LoginControlador:
    """
    Clase: LoginControlador
    Descripción: Recibe lo que el usuario escribe en la pantalla de
    inicio de sesión, comprueba los datos y decide qué hacer.
    """

    def __init__(self, vista, modelo, sesion):
        self.vista = vista
        self.modelo = modelo
        self.sesion = sesion

    def iniciar_sesion(self, nombre_usuario, contrasena):
        nombre_usuario = nombre_usuario.strip()

        if nombre_usuario == "" or contrasena == "":
            self.vista.mostrar_error("Debe completar el usuario y la contraseña")
            return

                # Caso 2: el usuario no existe
        try:
            usuario = self.modelo.buscar_por_nombre_usuario(nombre_usuario)
        except ConnectionError:
            self.vista.mostrar_error(
                "No se pudo conectar con la base de datos. "
                "Verifique que MySQL esté encendido."
            )
            return

        if usuario is None:
            self.vista.mostrar_error("Usuario o contraseña incorrectos")
            return

        if self.modelo.verificar_contrasena(contrasena, usuario["hash"]):
            self.sesion.guardar(usuario["id"], usuario["nombre"], usuario["rol"])
            self.vista.abrir_pantalla_principal()
        else:
            self.vista.mostrar_error("Usuario o contraseña incorrectos")