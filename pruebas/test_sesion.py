import unittest

from modelo.sesion import Sesion


class PruebasSesion(unittest.TestCase):

    def test_al_crearse_no_hay_sesion(self):
        sesion = Sesion()
        self.assertFalse(sesion.hay_sesion_iniciada())
        self.assertIsNone(sesion.obtener_id())

    def test_guardar_deja_los_datos_del_usuario(self):
        sesion = Sesion()
        sesion.guardar(3, "Ana López", "administrador")
        self.assertTrue(sesion.hay_sesion_iniciada())
        self.assertEqual(sesion.obtener_id(), 3)
        self.assertEqual(sesion.obtener_nombre(), "Ana López")
        self.assertEqual(sesion.obtener_rol(), "administrador")


if __name__ == "__main__":
    unittest.main()
