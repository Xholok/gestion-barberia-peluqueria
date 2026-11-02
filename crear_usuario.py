import bcrypt
import mysql.connector


def solo_digitos(texto):
    """
    Revisa que el texto tenga únicamente números del 0 al 9.
    Devuelve True si es así y False si no.
    """
    for caracter in texto:
        if caracter not in "0123456789":
            return False
    return True


def pedir_dato_obligatorio(mensaje):
    """
    Pide un dato por teclado y lo vuelve a pedir mientras esté vacío.
    """
    dato = input(mensaje).strip()
    while dato == "":
        print("Este dato es obligatorio.")
        dato = input(mensaje).strip()
    return dato


def pedir_telefono():
    """
    Pide el teléfono y lo vuelve a pedir hasta que tenga exactamente 10 números.
    """
    telefono = input("Teléfono (10 dígitos): ").strip()
    while len(telefono) != 10 or not solo_digitos(telefono):
        print("El teléfono debe tener exactamente 10 dígitos, solo números.")
        telefono = input("Teléfono (10 dígitos): ").strip()
    return telefono


def pedir_rol():
    """
    Pide el rol y lo vuelve a pedir hasta que sea uno de los tres que existen.
    """
    roles_validos = ["administrador", "barbero", "peluquero"]
    rol = input("Rol (administrador / barbero / peluquero): ").strip().lower()
    while rol not in roles_validos:
        print("Escriba exactamente: administrador, barbero o peluquero.")
        rol = input("Rol (administrador / barbero / peluquero): ").strip().lower()
    return rol


def crear_usuario(nombres, apellidos, telefono, nombre_usuario, contrasena, rol):
    """
    Guarda en la base de datos a la persona y a su usuario.
    La contraseña nunca se guarda tal cual: se convierte en hash con bcrypt.
    Si algo falla, no queda nada guardado a medias.
    """
    hash_contrasena = bcrypt.hashpw(
        contrasena.encode("utf-8"), bcrypt.gensalt()
    ).decode("utf-8")

    conexion = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="",
        database="barberia"
    )
    cursor = conexion.cursor()

    try:
        # Buscar el id del rol escrito
        cursor.execute("SELECT id_rol FROM rol WHERE nombre_rol = %s", (rol,))
        fila_rol = cursor.fetchone()

        if fila_rol is None:
            print("Ese rol no existe en la base de datos.")
            return

        id_rol = fila_rol[0]

        # Primero se guarda la persona
        cursor.execute(
            "INSERT INTO persona (nombres, apellidos, telefono) VALUES (%s, %s, %s)",
            (nombres, apellidos, telefono)
        )
        id_persona = cursor.lastrowid

        # Después el usuario, enlazado a esa persona
        cursor.execute(
            "INSERT INTO usuario (id_persona, nombre_usuario, contrasena_hash, id_rol) "
            "VALUES (%s, %s, %s, %s)",
            (id_persona, nombre_usuario, hash_contrasena, id_rol)
        )

        conexion.commit()
        print("Usuario creado correctamente.")

    except mysql.connector.IntegrityError:
        conexion.rollback()
        print("No se pudo crear: ese teléfono o ese nombre de usuario ya existen.")
    except mysql.connector.Error as error:
        conexion.rollback()
        print("No se pudo crear el usuario:", error)
    finally:
        cursor.close()
        conexion.close()


def main():
    print("=== Crear usuarios ===")
    seguir = "s"

    while seguir == "s":
        nombres = pedir_dato_obligatorio("Nombres: ")
        apellidos = input("Apellidos (Enter si no tiene): ").strip()
        if apellidos == "":
            apellidos = None
        telefono = pedir_telefono()
        nombre_usuario = pedir_dato_obligatorio("Nombre de usuario: ")
        contrasena = pedir_dato_obligatorio("Contraseña: ")
        rol = pedir_rol()

        crear_usuario(nombres, apellidos, telefono, nombre_usuario, contrasena, rol)

        seguir = input("¿Crear otro usuario? (s/n): ").strip().lower()


if __name__ == "__main__":
    main()