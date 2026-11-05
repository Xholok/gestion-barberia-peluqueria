import unittest

from controlador.cliente_controlador import ClienteControlador
from modelo.cliente_modelo import TelefonoRepetidoError
from pruebas.dobles import VistaFalsa, SesionFalsa, ClienteModeloFalso

TELEFONO_BUENO = "3157778899"


class PruebasClienteControlador(unittest.TestCase):

    def preparar(self, telefonos=None, error_al_buscar=None, error_al_guardar=None,
                 sesion=None, respuesta_confirmar=True):
        self.vista = VistaFalsa(respuesta_confirmar)
        self.modelo = ClienteModeloFalso(telefonos, error_al_buscar, error_al_guardar)
        if sesion is None:
            sesion = SesionFalsa()
        self.sesion = sesion
        self.controlador = ClienteControlador(self.vista, self.modelo, self.sesion)

    def registrar(self, nombre="Pedro Ramírez", telefono=TELEFONO_BUENO, usa_whatsapp=True,
                  observaciones="", autoriza=True):
        self.controlador.registrar_cliente(nombre, telefono, usa_whatsapp, observaciones, autoriza)

    def error_de(self, campo):
        if self.vista.errores is None:
            return None
        return self.vista.errores.get(campo)

    # ---------------- Sesión (RF-01) ----------------
    def test_sin_sesion_no_guarda(self):
        self.preparar(sesion=SesionFalsa(id_usuario=None))
        self.registrar()
        self.assertIn("iniciar sesión", self.vista.error_general)
        self.assertEqual(self.modelo.guardados, [])

    # ---------------- Nombre (RF-03 a RF-06) ----------------
    def test_nombre_vacio(self):
        self.preparar()
        self.registrar(nombre="")
        self.assertEqual(self.error_de("nombre"), "El nombre es obligatorio.")

    def test_nombre_solo_espacios_es_vacio(self):
        self.preparar()
        self.registrar(nombre="     ")
        self.assertEqual(self.error_de("nombre"), "El nombre es obligatorio.")

    def test_nombre_de_1_caracter_rechazado(self):
        self.preparar()
        self.registrar(nombre="A")
        self.assertIn("entre 2 y 60", self.error_de("nombre"))

    def test_nombre_de_2_caracteres_aceptado(self):
        self.preparar()
        self.registrar(nombre="Al")
        self.assertIsNone(self.vista.errores)
        self.assertEqual(len(self.modelo.guardados), 1)

    def test_nombre_de_60_caracteres_aceptado(self):
        self.preparar()
        self.registrar(nombre="a" * 60)
        self.assertEqual(len(self.modelo.guardados), 1)

    def test_nombre_de_61_caracteres_rechazado(self):
        self.preparar()
        self.registrar(nombre="a" * 61)
        self.assertIn("entre 2 y 60", self.error_de("nombre"))

    def test_nombre_con_tildes_enie_y_dieresis_aceptado(self):
        self.preparar()
        self.registrar(nombre="José Peña Güell")
        self.assertEqual(self.modelo.guardados[0]["nombre"], "José Peña Güell")

    def test_nombre_con_numero_rechazado(self):
        self.preparar()
        self.registrar(nombre="Juan3")
        self.assertEqual(self.error_de("nombre"), "El nombre solo puede tener letras y espacios.")

    def test_nombre_con_simbolo_rechazado(self):
        self.preparar()
        self.registrar(nombre="Ana@")
        self.assertEqual(self.error_de("nombre"), "El nombre solo puede tener letras y espacios.")

    def test_nombre_con_espacios_de_mas_se_limpia(self):
        self.preparar()
        self.registrar(nombre="  Juan   Pérez  ")
        self.assertEqual(self.modelo.guardados[0]["nombre"], "Juan Pérez")

    # ---------------- Teléfono (RF-07 a RF-10) ----------------
    def test_telefono_vacio(self):
        self.preparar()
        self.registrar(telefono="")
        self.assertEqual(self.error_de("telefono"), "El teléfono es obligatorio.")

    def test_telefono_de_9_digitos(self):
        self.preparar()
        self.registrar(telefono="315777889")
        self.assertIn("exactamente 10 dígitos", self.error_de("telefono"))

    def test_telefono_de_11_digitos(self):
        self.preparar()
        self.registrar(telefono="31577788990")
        self.assertIn("exactamente 10 dígitos", self.error_de("telefono"))

    def test_telefono_con_letras(self):
        self.preparar()
        self.registrar(telefono="31577788AB")
        self.assertIn("exactamente 10 dígitos", self.error_de("telefono"))

    def test_telefono_con_espacios(self):
        self.preparar()
        self.registrar(telefono="315 777 889")
        self.assertIn("exactamente 10 dígitos", self.error_de("telefono"))

    def test_telefono_que_no_empieza_por_3(self):
        self.preparar()
        self.registrar(telefono="2101234567")
        self.assertEqual(self.error_de("telefono"), "El teléfono debe empezar por 3.")

    def test_telefono_de_otro_cliente(self):
        self.preparar(telefonos={TELEFONO_BUENO: {"nombre": "Carlos Gómez", "es_cliente": True, "es_usuario": False}})
        self.registrar()
        self.assertIn("Carlos Gómez", self.error_de("telefono"))
        self.assertEqual(self.modelo.guardados, [])

    def test_telefono_de_un_usuario_si_se_registra(self):
        # Un barbero puede ser cliente del local
        self.preparar(telefonos={TELEFONO_BUENO: {"nombre": "Ivan David", "es_cliente": False, "es_usuario": True}})
        self.registrar(nombre="David")
        self.assertEqual(len(self.modelo.guardados), 1)
        self.assertIn("Ivan David", self.vista.exito)
        self.assertIn("usuario del sistema", self.vista.exito)

    # ---------------- WhatsApp y observaciones (RF-11, RF-12) ----------------
    def test_whatsapp_no_se_guarda(self):
        self.preparar()
        self.registrar(usa_whatsapp=False)
        self.assertFalse(self.modelo.guardados[0]["usa_whatsapp"])

    def test_observaciones_vacias_se_guardan_como_none(self):
        self.preparar()
        self.registrar(observaciones="   ")
        self.assertIsNone(self.modelo.guardados[0]["observaciones"])

    def test_observaciones_de_200_caracteres_aceptadas(self):
        self.preparar()
        self.registrar(observaciones="x" * 200)
        self.assertEqual(len(self.modelo.guardados), 1)

    def test_observaciones_de_201_caracteres_rechazadas(self):
        self.preparar()
        self.registrar(observaciones="x" * 201)
        self.assertIn("200", self.error_de("observaciones"))

    # ---------------- Autorización (RF-13) ----------------
    def test_sin_autorizacion_no_guarda(self):
        self.preparar()
        self.registrar(autoriza=False)
        self.assertIsNotNone(self.error_de("autorizacion"))
        self.assertEqual(self.modelo.guardados, [])

    # ---------------- Varios errores a la vez (RF-18, RF-19) ----------------
    def test_muestra_todos_los_errores_juntos_y_no_guarda(self):
        self.preparar()
        self.registrar(nombre="", telefono="123", autoriza=False)
        self.assertEqual(set(self.vista.errores.keys()), {"nombre", "telefono", "autorizacion"})
        self.assertEqual(self.modelo.guardados, [])
        self.assertNotIn("limpiar_formulario", self.vista.acciones)

    # ---------------- Registro correcto (RF-14 a RF-17, RF-20) ----------------
    def test_registro_correcto(self):
        self.preparar()
        self.registrar()
        guardado = self.modelo.guardados[0]
        self.assertEqual(guardado["id_usuario_registro"], 7)
        self.assertTrue(guardado["autoriza_datos"])
        self.assertIn("Cliente registrado", self.vista.exito)
        self.assertIn("CL-0001", self.vista.exito)
        self.assertIn("04/11/2026 10:30", self.vista.exito)
        self.assertIn("Registrado por: Juan Pérez", self.vista.exito)
        self.assertIn("Estado: Activo", self.vista.exito)
        self.assertIn("limpiar_formulario", self.vista.acciones)

    # ---------------- Base de datos (E3 y E4 del caso de uso) ----------------
    def test_base_de_datos_apagada_al_buscar(self):
        self.preparar(error_al_buscar=ConnectionError())
        self.registrar()
        self.assertIn("No se pudo conectar", self.vista.error_general)
        self.assertEqual(self.modelo.guardados, [])

    def test_base_de_datos_apagada_al_guardar(self):
        self.preparar(error_al_guardar=ConnectionError())
        self.registrar()
        self.assertIn("No se pudo guardar", self.vista.error_general)
        self.assertIsNone(self.vista.exito)

    def test_otro_usuario_registro_el_telefono_justo_antes(self):
        self.preparar(error_al_guardar=TelefonoRepetidoError())
        self.registrar()
        self.assertIn("ya está registrado", self.error_de("telefono"))
        self.assertIsNone(self.vista.exito)

    # ---------------- Cancelar (RF-21) ----------------
    def test_cancelar_sin_datos_vuelve_sin_preguntar(self):
        self.preparar()
        self.controlador.cancelar(False)
        self.assertEqual(self.vista.acciones, ["volver_a_gestion"])

    def test_cancelar_con_datos_y_acepta(self):
        self.preparar(respuesta_confirmar=True)
        self.controlador.cancelar(True)
        self.assertEqual(self.vista.acciones, ["confirmar_descartar", "volver_a_gestion"])

    def test_cancelar_con_datos_y_no_acepta(self):
        self.preparar(respuesta_confirmar=False)
        self.controlador.cancelar(True)
        self.assertEqual(self.vista.acciones, ["confirmar_descartar"])


if __name__ == "__main__":
    unittest.main()
