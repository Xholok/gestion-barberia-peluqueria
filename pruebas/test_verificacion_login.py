import unittest
from unittest import mock

import bcrypt
import mysql.connector

from modelo.verificacion_login import VerificacionLogin


class PruebasVerificacionLogin(unittest.TestCase):

    def setUp(self):
        self.modelo = VerificacionLogin()
        self.hash = bcrypt.hashpw("clave123".encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def test_contrasena_correcta(self):
        self.assertTrue(self.modelo.verificar_contrasena("clave123", self.hash))

    def test_contrasena_incorrecta(self):
        self.assertFalse(self.modelo.verificar_contrasena("clave124", self.hash))

    def test_distingue_mayusculas(self):
        self.assertFalse(self.modelo.verificar_contrasena("CLAVE123", self.hash))

    def test_base_de_datos_apagada_lanza_connection_error(self):
        # Se simula que MySQL no responde, sin apagarlo de verdad
        falla = mysql.connector.Error("MySQL apagado")
        with mock.patch("mysql.connector.connect", side_effect=falla):
            with self.assertRaises(ConnectionError):
                self.modelo.buscar_por_nombre_usuario("juan")


if __name__ == "__main__":
    unittest.main()
