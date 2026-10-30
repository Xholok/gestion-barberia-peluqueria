import bcrypt
import mysql.connector

print("=== Crear usuario ===")
nombres = input("Nombres: ")
apellidos = input("Apellidos (Enter si no tiene): ")
telefono = input("Teléfono: ")
nombre_usuario = input("Nombre de usuario: ")
contrasena = input("Contraseña: ")
rol = input("Rol (administrador / barbero / peluquero): ")

if apellidos == "":
    apellidos = None

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
    cursor.execute("SELECT id_rol FROM rol WHERE nombre_rol = %s", (rol,))
    fila_rol = cursor.fetchone()

    if fila_rol is None:
        print("Ese rol no existe.")
    else:
        id_rol = fila_rol[0]

        cursor.execute(
            "INSERT INTO persona (nombres, apellidos, telefono) VALUES (%s, %s, %s)",
            (nombres, apellidos, telefono)
        )
        id_persona = cursor.lastrowid

        cursor.execute(
            "INSERT INTO usuario (id_persona, nombre_usuario, contrasena_hash, id_rol) "
            "VALUES (%s, %s, %s, %s)",
            (id_persona, nombre_usuario, hash_contrasena, id_rol)
        )

        conexion.commit()
        print("Usuario creado correctamente.")

except mysql.connector.Error as error:
    conexion.rollback()
    print("No se pudo crear el usuario:", error)

cursor.close()
conexion.close()