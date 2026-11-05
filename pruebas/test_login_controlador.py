import unittest

from controlador.login_controlador import LoginControlador
from pruebas.dobles import VistaFalsa, SesionFalsa, LoginModeloFalso

USUARIOS = {"juan": {"id": 1, "nombre": "Juan Pérez", "rol": "barbero", "hash": "clave123"}}
MENSAJE_INCORRECTO = "Usuario o contraseña incorrectos"


class PruebasLoginControlador(unittest.TestCase):

    def preparar(self, error=None):
        self.vista = VistaFalsa()
        self.sesion = SesionFalsa(id_usuario=None)
        modelo = LoginModeloFalso(USUARIOS, error)
        self.controlador = LoginControlador(self.vista, modelo, self.sesion)

    def test_campos_vacios(self):
        self.preparar()
        self.controlador.iniciar_sesion("", "")
        self.assertEqual(self.vista.error_general, "Debe completar el usuario y la contraseña")
        self.assertIsNone(self.sesion.guardado)

    def test_usuario_con_solo_espacios_cuenta_como_vacio(self):
        self.preparar()
        self.controlador.iniciar_sesion("   ", "clave123")
        self.assertEqual(self.vista.error_general, "Debe completar el usuario y la contraseña")

    def test_usuario_que_no_existe(self):
        self.preparar()
        self.controlador.iniciar_sesion("nadie", "clave123")
        self.assertEqual(self.vista.error_general, MENSAJE_INCORRECTO)
        self.assertIsNone(self.sesion.guardado)

    def test_contrasena_incorrecta_usa_el_mismo_mensaje(self):
        # Mismo mensaje que "no existe": así no se revela qué usuarios existen
        self.preparar()
        self.controlador.iniciar_sesion("juan", "otra")
        self.assertEqual(self.vista.error_general, MENSAJE_INCORRECTO)
        self.assertIsNone(self.sesion.guardado)

    def test_datos_correctos_guardan_sesion_y_abren_el_panel(self):
        self.preparar()
        self.controlador.iniciar_sesion("  juan ", "clave123")
        self.assertEqual(self.sesion.guardado, (1, "Juan Pérez", "barbero"))
        self.assertIn("abrir_pantalla_principal", self.vista.acciones)
        self.assertIsNone(self.vista.error_general)

    def test_base_de_datos_apagada(self):
        self.preparar(error=ConnectionError())
        self.controlador.iniciar_sesion("juan", "clave123")
        self.assertIn("No se pudo conectar", self.vista.error_general)
        self.assertIsNone(self.sesion.guardado)


if __name__ == "__main__":
    unittest.main()
