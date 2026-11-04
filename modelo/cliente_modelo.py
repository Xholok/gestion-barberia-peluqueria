import mysql.connector


class TelefonoRepetidoError(Exception):
    """
    Se lanza cuando el teléfono ya pertenece a otro cliente.
    """
    pass


class ClienteModelo:
    """
    Clase: ClienteModelo
    Descripción: Se encarga de los datos de los clientes en la base de datos:
    revisar si un teléfono ya está registrado y guardar un cliente nuevo.
    Un usuario del sistema (barbero, peluquero o administrador) también puede
    ser cliente: en ese caso se usan sus datos de persona que ya existen.
    Si no se puede usar la base de datos, avisa con un ConnectionError.
    """

    def generar_codigo(self, id_cliente):
        """
        Convierte el número interno del cliente en su código visible.
        Ejemplo: 1 se convierte en CL-0001.
        """
        return "CL-" + str(id_cliente).zfill(4)

    def buscar_por_telefono(self, telefono):
        """
        Busca en la tabla persona (usuarios y clientes) quién tiene ese teléfono.
        Devuelve un diccionario con el nombre, si ya es cliente y si es usuario,
        o None si el teléfono no está registrado.
        """
        try:
            conexion = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="",
                database="barberia"
            )
            cursor = conexion.cursor()

            consulta = (
                "SELECT p.nombres, c.id_cliente, u.id_usuario "
                "FROM persona p "
                "LEFT JOIN cliente c ON c.id_persona = p.id_persona "
                "LEFT JOIN usuario u ON u.id_persona = p.id_persona "
                "WHERE p.telefono = %s"
            )
            cursor.execute(consulta, (telefono,))
            fila = cursor.fetchone()

            cursor.close()
            conexion.close()
        except mysql.connector.Error:
            raise ConnectionError("No se pudo acceder a la base de datos")

        if fila is None:
            return None

        resultado = {
            "nombre": fila[0],
            "es_cliente": fila[1] is not None,
            "es_usuario": fila[2] is not None
        }
        return resultado

    def guardar_cliente(self, nombre, telefono, usa_whatsapp, observaciones,
                        autoriza_datos, id_usuario_registro):
        """
        Guarda al cliente. Si el teléfono ya pertenece a un usuario que todavía
        no es cliente, se usa esa misma persona en lugar de crear otra.
        Si algo falla, no queda nada guardado a medias.
        Devuelve un diccionario con el código, la fecha, el nombre guardado
        y si se vinculó con un usuario existente.
        Lanza TelefonoRepetidoError si el teléfono ya es de otro cliente.
        """
        conexion = None
        try:
            conexion = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="",
                database="barberia"
            )
            cursor = conexion.cursor()

            cursor.execute(
                "SELECT p.id_persona, p.nombres, c.id_cliente "
                "FROM persona p "
                "LEFT JOIN cliente c ON c.id_persona = p.id_persona "
                "WHERE p.telefono = %s FOR UPDATE",
                (telefono,)
            )
            fila = cursor.fetchone()

            vinculado_a_usuario = False
            if fila is None:
                cursor.execute(
                    "INSERT INTO persona (nombres, apellidos, telefono) VALUES (%s, NULL, %s)",
                    (nombre, telefono)
                )
                id_persona = cursor.lastrowid
                nombre_guardado = nombre
            elif fila[2] is not None:
                conexion.rollback()
                raise TelefonoRepetidoError()
            else:
                id_persona = fila[0]
                nombre_guardado = fila[1]
                vinculado_a_usuario = True

            cursor.execute(
                "INSERT INTO cliente (id_persona, usa_whatsapp, observaciones, "
                "autoriza_datos, id_usuario_registro) VALUES (%s, %s, %s, %s, %s)",
                (id_persona, usa_whatsapp, observaciones, autoriza_datos, id_usuario_registro)
            )
            id_cliente = cursor.lastrowid

            cursor.execute(
                "SELECT fecha_registro FROM cliente WHERE id_cliente = %s",
                (id_cliente,)
            )
            fecha_registro = cursor.fetchone()[0]

            conexion.commit()
            cursor.close()
        except mysql.connector.IntegrityError as error:
            conexion.rollback()
            if error.errno == 1062:
                raise TelefonoRepetidoError()
            raise ConnectionError("No se pudo guardar el cliente")
        except mysql.connector.Error:
            if conexion is not None and conexion.is_connected():
                conexion.rollback()
            raise ConnectionError("No se pudo guardar el cliente")
        finally:
            if conexion is not None and conexion.is_connected():
                conexion.close()

        resultado = {
            "codigo": self.generar_codigo(id_cliente),
            "fecha_registro": fecha_registro,
            "nombre": nombre_guardado,
            "vinculado_a_usuario": vinculado_a_usuario
        }
        return resultado