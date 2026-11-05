"""
Objetos de mentira ("dobles") para las pruebas unitarias.
Reemplazan la ventana, la base de datos y la sesión, así cada prueba revisa
una sola clase sin abrir ventanas ni tocar MySQL. Cada doble anota lo que
le pidieron hacer para que la prueba pueda revisarlo después.
"""
from datetime import datetime


class SesionFalsa:
    def __init__(self, id_usuario=7, nombre="Juan Pérez", rol="barbero"):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.rol = rol
        self.guardado = None

    def hay_sesion_iniciada(self):
        return self.id_usuario is not None

    def obtener_id(self):
        return self.id_usuario

    def obtener_nombre(self):
        return self.nombre

    def obtener_rol(self):
        return self.rol

    def guardar(self, id, nombre, rol):
        self.guardado = (id, nombre, rol)


class VistaFalsa:
    """Sirve para el login, el registro de clientes y la gestión de clientes."""

    def __init__(self, respuesta_confirmar=True):
        self.respuesta_confirmar = respuesta_confirmar
        self.errores = None
        self.error_general = None
        self.exito = None
        self.avisos = []
        self.acciones = []

    # Login
    def mostrar_error(self, mensaje):
        self.error_general = mensaje

    def abrir_pantalla_principal(self):
        self.acciones.append("abrir_pantalla_principal")

    # Registro de cliente
    def mostrar_errores(self, errores):
        self.errores = errores

    def mostrar_error_general(self, mensaje):
        self.error_general = mensaje

    def mostrar_exito(self, mensaje):
        self.exito = mensaje

    def limpiar_formulario(self):
        self.acciones.append("limpiar_formulario")

    def confirmar_descartar(self):
        self.acciones.append("confirmar_descartar")
        return self.respuesta_confirmar

    def volver_a_gestion(self):
        self.acciones.append("volver_a_gestion")

    # Gestión de clientes y panel
    def mostrar_aviso(self, mensaje):
        self.avisos.append(mensaje)

    def abrir_formulario_registro(self):
        self.acciones.append("abrir_formulario_registro")

    def solicitar_inicio_sesion(self):
        self.acciones.append("solicitar_inicio_sesion")

    def volver_al_panel(self):
        self.acciones.append("volver_al_panel")

    def mostrar_usuario(self, nombre, rol):
        self.acciones.append(("mostrar_usuario", nombre, rol))

    def mostrar_fecha(self, texto):
        self.acciones.append(("mostrar_fecha", texto))

    def abrir_gestion_clientes(self):
        self.acciones.append("abrir_gestion_clientes")


class ClienteModeloFalso:
    """
    Simula la base de datos de clientes.
    telefonos: diccionario teléfono -> {"nombre", "es_cliente", "es_usuario"}
    error_al_buscar / error_al_guardar: excepción que se lanza a propósito.
    """

    def __init__(self, telefonos=None, error_al_buscar=None, error_al_guardar=None):
        self.telefonos = telefonos if telefonos is not None else {}
        self.error_al_buscar = error_al_buscar
        self.error_al_guardar = error_al_guardar
        self.guardados = []

    def buscar_por_telefono(self, telefono):
        if self.error_al_buscar is not None:
            raise self.error_al_buscar
        return self.telefonos.get(telefono)

    def guardar_cliente(self, nombre, telefono, usa_whatsapp, observaciones,
                        autoriza_datos, id_usuario_registro):
        if self.error_al_guardar is not None:
            raise self.error_al_guardar
        self.guardados.append({
            "nombre": nombre, "telefono": telefono, "usa_whatsapp": usa_whatsapp,
            "observaciones": observaciones, "autoriza_datos": autoriza_datos,
            "id_usuario_registro": id_usuario_registro
        })
        existente = self.telefonos.get(telefono)
        vinculado = existente is not None
        nombre_guardado = nombre
        if vinculado:
            nombre_guardado = existente["nombre"]
        return {
            "codigo": "CL-" + str(len(self.guardados)).zfill(4),
            "fecha_registro": datetime(2026, 11, 4, 10, 30),
            "nombre": nombre_guardado,
            "vinculado_a_usuario": vinculado
        }


class LoginModeloFalso:
    def __init__(self, usuarios=None, error=None):
        self.usuarios = usuarios if usuarios is not None else {}
        self.error = error

    def buscar_por_nombre_usuario(self, nombre_usuario):
        if self.error is not None:
            raise self.error
        return self.usuarios.get(nombre_usuario)

    def verificar_contrasena(self, contrasena, hash):
        return contrasena == hash
