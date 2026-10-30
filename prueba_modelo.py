from modelo.verificacion_login import VerificacionLogin
from modelo.sesion import Sesion
from controlador.login_controlador import LoginControlador


class VistaFalsa:
    """Vista de mentira: solo imprime lo que haría la pantalla real."""

    def mostrar_error(self, mensaje):
        print("ERROR EN PANTALLA:", mensaje)

    def abrir_pantalla_principal(self):
        print("SE ABRE LA PANTALLA PRINCIPAL")


sesion = Sesion()
controlador = LoginControlador(VistaFalsa(), VerificacionLogin(), sesion)

nombre_usuario = input("Usuario: ")
contrasena = input("Contraseña: ")
controlador.iniciar_sesion(nombre_usuario, contrasena)

print("Sesión iniciada:", sesion.hay_sesion_iniciada())
if sesion.hay_sesion_iniciada():
    print("Nombre:", sesion.obtener_nombre(), "- Rol:", sesion.obtener_rol())