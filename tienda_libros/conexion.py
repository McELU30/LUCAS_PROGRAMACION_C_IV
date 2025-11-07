import mysql.connector

def conectar():
    try:
        conexion = mysql.connector.connect(
            host="localhost",        # o la IP del servidor MySQL
            user="root",             # ⚠️ Tu usuario MySQL
            password="", # ⚠️ Tu contraseña de MySQL
            database="tienda_libros" # ⚠️ Tu base de datos
        )

        if conexion.is_connected():
            print("✅ Conexión establecida con la base de datos tienda_libros")
        return conexion

    except mysql.connector.Error as err:
        print(f"❌ Error al conectar con la base de datos: {err}")
        return None