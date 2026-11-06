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

    def test_busqueda_escapa_porcentaje_y_guion_bajo(self):
        # Se revisan los parámetros que el modelo le manda a MySQL, sin MySQL real
        conexion = mock.MagicMock()
        cursor = conexion.cursor.return_value
        cursor.fetchall.return_value = []
        with mock.patch("mysql.connector.connect", return_value=conexion):
            self.modelo.listar_clientes(" 50%_ ", 50)
        parametros = cursor.execute.call_args[0][1]
        self.assertEqual(parametros, ("50\\%\\_%", "% 50\\%\\_%", "50\\%\\_%", 50))

    def test_lista_une_nombres_y_apellidos(self):
        conexion = mock.MagicMock()
        cursor = conexion.cursor.return_value
        cursor.fetchall.return_value = [("Ivan", "David", "3103356105"), ("Ana", None, "3001110001")]
        with mock.patch("mysql.connector.connect", return_value=conexion):
            clientes = self.modelo.listar_clientes("", 50)
        self.assertEqual(clientes[0], {"nombre": "Ivan David", "telefono": "3103356105"})
        self.assertEqual(clientes[1]["nombre"], "Ana")

    def test_base_de_datos_apagada_al_listar(self):
        falla = mysql.connector.Error("MySQL apagado")
        with mock.patch("mysql.connector.connect", side_effect=falla):
            with self.assertRaises(ConnectionError):
                self.modelo.listar_clientes("", 50)


if __name__ == "__main__":
    unittest.main()
