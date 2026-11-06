import bcrypt
import mysql.connector

class VerificacionLogin:
    """
    Clase: VerificacionLogin
    Descripción: Se encarga de buscar a los usuarios en la base de datos
    y de comprobar si la contraseña escrita es la correcta.
    """

    def buscar_por_nombre_usuario(self, nombre_usuario):
        """
        Busca un usuario por su nombre de usuario.
        Devuelve un diccionario con su id, su nombre, su rol y su hash,
        o None si el usuario no existe.
        Si no se puede usar la base de datos, avisa con un ConnectionError.
        """
        try:
            conexion = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="",
                database="barberia",
                use_pure=True
            )
            cursor = conexion.cursor()

            consulta = (
                "SELECT u.id_usuario, p.nombres, p.apellidos, r.nombre_rol, u.contrasena_hash "
                "FROM usuario u "
                "INNER JOIN persona p ON u.id_persona = p.id_persona "
                "INNER JOIN rol r ON u.id_rol = r.id_rol "
                "WHERE u.nombre_usuario = %s"
            )
            cursor.execute(consulta, (nombre_usuario,))
            fila = cursor.fetchone()

            cursor.close()
            conexion.close()
        except mysql.connector.Error:
            raise ConnectionError("No se pudo acceder a la base de datos")

        if fila is None:
            return None

        if fila[2] is None:
            nombre_completo = fila[1]
        else:
            nombre_completo = fila[1] + " " + fila[2]

        usuario = {
            "id": fila[0],
            "nombre": nombre_completo,
            "rol": fila[3],
            "hash": fila[4]
        }
        return usuario

    def verificar_contrasena(self, contrasena, hash):
        """
        Comprueba si la contraseña escrita corresponde al hash guardado.
        Devuelve True si coincide y False si no.
        """
        contrasena_bytes = contrasena.encode("utf-8")
        hash_bytes = hash.encode("utf-8")
        return bcrypt.checkpw(contrasena_bytes, hash_bytes)