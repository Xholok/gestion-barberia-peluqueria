import unittest

from controlador.lista_clientes_controlador import ListaClientesControlador, LIMITE_RESULTADOS
from pruebas.dobles import VistaFalsa, ClienteModeloFalso

CLIENTES = [{"nombre": "José Pérez", "telefono": "3001110001"},
            {"nombre": "Juliana Ríos", "telefono": "3001110002"}]


class PruebasListaClientesControlador(unittest.TestCase):

    def preparar(self, lista=None, error=None):
        self.vista = VistaFalsa()
        self.modelo = ClienteModeloFalso(lista=lista, error_al_buscar=error)
        self.controlador = ListaClientesControlador(self.vista, self.modelo)

    def test_al_abrir_muestra_los_recientes(self):
        self.preparar(CLIENTES)
        self.controlador.mostrar_recientes()
        self.assertEqual(self.modelo.busquedas, [("", LIMITE_RESULTADOS)])
        self.assertEqual(self.vista.clientes_mostrados, CLIENTES)
        self.assertIn("más recientemente", self.vista.estado)

    def test_sin_clientes_registrados(self):
        self.preparar([])
        self.controlador.mostrar_recientes()
        self.assertEqual(self.vista.estado, "Aún no hay clientes registrados.")

    def test_busqueda_quita_espacios_y_cuenta_resultados(self):
        self.preparar(CLIENTES)
        self.controlador.buscar("  j ")
        self.assertEqual(self.modelo.busquedas[0][0], "j")
        self.assertEqual(self.vista.estado, "2 clientes encontrados para «j».")

    def test_busqueda_con_un_resultado(self):
        self.preparar(CLIENTES[:1])
        self.controlador.buscar("jose")
        self.assertEqual(self.vista.estado, "1 cliente encontrado para «jose».")

    def test_busqueda_sin_resultados(self):
        self.preparar([])
        self.controlador.buscar("zzz")
        self.assertEqual(self.vista.clientes_mostrados, [])
        self.assertEqual(self.vista.estado, "No se encontraron clientes para «zzz».")

    def test_busqueda_que_llega_al_limite_sugiere_afinar(self):
        muchos = [{"nombre": "Cliente", "telefono": "3000000000"}] * (LIMITE_RESULTADOS + 5)
        self.preparar(muchos)
        self.controlador.buscar("c")
        self.assertEqual(len(self.vista.clientes_mostrados), LIMITE_RESULTADOS)
        self.assertIn("afinar", self.vista.estado)

    def test_base_de_datos_apagada(self):
        self.preparar(error=ConnectionError())
        self.controlador.buscar("j")
        self.assertEqual(self.vista.clientes_mostrados, [])
        self.assertIn("No se pudo conectar", self.vista.estado)

    def test_volver(self):
        self.preparar()
        self.controlador.volver()
        self.assertEqual(self.vista.acciones, ["volver_a_gestion"])


if __name__ == "__main__":
    unittest.main()
