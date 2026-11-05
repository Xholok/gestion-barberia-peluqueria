import unittest
from datetime import date
from unittest import mock

from controlador.panel_principal_controlador import PanelPrincipalControlador
from pruebas.dobles import VistaFalsa, SesionFalsa


class PruebasPanelPrincipalControlador(unittest.TestCase):

    def test_muestra_usuario_rol_y_fecha_en_espanol(self):
        vista = VistaFalsa()
        controlador = PanelPrincipalControlador(vista, SesionFalsa(nombre="Ana López", rol="administrador"))
        # Se fija la fecha para que la prueba no dependa del día en que se ejecuta
        with mock.patch("controlador.panel_principal_controlador.date") as fecha_falsa:
            fecha_falsa.today.return_value = date(2026, 11, 4)
            controlador.mostrar_panel()
        self.assertIn(("mostrar_usuario", "Ana López", "administrador"), vista.acciones)
        self.assertIn(("mostrar_fecha", "Miércoles, 4 de noviembre de 2026"), vista.acciones)

    def test_boton_clientes_abre_gestion(self):
        vista = VistaFalsa()
        PanelPrincipalControlador(vista, SesionFalsa()).abrir_modulo_clientes()
        self.assertEqual(vista.acciones, ["abrir_gestion_clientes"])


if __name__ == "__main__":
    unittest.main()
