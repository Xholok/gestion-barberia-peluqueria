import unittest
from unittest import mock

import mysql.connector

from modelo.cliente_modelo import ClienteModelo


class PruebasClienteModelo(unittest.TestCase):

    def setUp(self):
        self.modelo = ClienteModelo()

    def test_codigo_con_cuatro_digitos(self):
        self.assertEqual(self.modelo.generar_codigo(1), "CL-0001")
        self.assertEqual(self.modelo.generar_codigo(25), "CL-0025")
        self.assertEqual(self.modelo.generar_codigo(9999), "CL-9999")

    def test_codigo_mayor_a_9999_no_se_corta(self):
        self.assertEqual(self.modelo.generar_codigo(12345), "CL-12345")

    def test_base_de_datos_apagada_al_buscar(self):
        falla = mysql.connector.Error("MySQL apagado")
        with mock.patch("mysql.connector.connect", side_effect=falla):
            with self.assertRaises(ConnectionError):
                self.modelo.buscar_por_telefono("3157778899")

    def test_base_de_datos_apagada_al_guardar(self):
        falla = mysql.connector.Error("MySQL apagado")
        with mock.patch("mysql.connector.connect", side_effect=falla):
            with self.assertRaises(ConnectionError):
                self.modelo.guardar_cliente("Pedro", "3157778899", True, None, True, 1)


if __name__ == "__main__":
    unittest.main()
