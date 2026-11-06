import unittest

from controlador.gestion_clientes_controlador import GestionClientesControlador
from pruebas.dobles import VistaFalsa, SesionFalsa


class PruebasGestionClientesControlador(unittest.TestCase):

    def abrir_con(self, sesion):
        vista = VistaFalsa()
        GestionClientesControlador(vista, sesion).abrir_registro_cliente()
        return vista

    def test_sin_sesion_pide_iniciar_sesion(self):
        vista = self.abrir_con(SesionFalsa(id_usuario=None))
        self.assertEqual(vista.acciones, ["solicitar_inicio_sesion"])

    def test_los_tres_roles_abren_el_formulario(self):
        for rol in ["administrador", "barbero", "peluquero"]:
            with self.subTest(rol=rol):
                vista = self.abrir_con(SesionFalsa(rol=rol))
                self.assertEqual(vista.acciones, ["abrir_formulario_registro"])

    def test_rol_desconocido_es_rechazado(self):
        vista = self.abrir_con(SesionFalsa(rol="invitado"))
        self.assertEqual(vista.acciones, [])
        self.assertIn("Acceso denegado", vista.avisos[0])

    def test_ver_lista_con_sesion(self):
        vista = VistaFalsa()
        GestionClientesControlador(vista, SesionFalsa()).abrir_lista_clientes()
        self.assertEqual(vista.acciones, ["abrir_lista"])

    def test_ver_lista_sin_sesion_pide_iniciar_sesion(self):
        vista = VistaFalsa()
        GestionClientesControlador(vista, SesionFalsa(id_usuario=None)).abrir_lista_clientes()
        self.assertEqual(vista.acciones, ["solicitar_inicio_sesion"])

    def test_volver_al_panel(self):
        vista = VistaFalsa()
        GestionClientesControlador(vista, SesionFalsa()).volver_al_panel()
        self.assertEqual(vista.acciones, ["volver_al_panel"])


if __name__ == "__main__":
    unittest.main()
