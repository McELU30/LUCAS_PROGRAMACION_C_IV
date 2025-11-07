# conexion.py
import mysql.connector
from mysql.connector import Error

class ConexionDB:
    def __init__(self):
        self.host = "localhost"
        self.user = "root"
        self.password = ""   # <- pon tu contraseña si la tienes
        self.database = "celular"

    def conectar(self):
        try:
            conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                autocommit=False
            )
            if conn.is_connected():
                return conn
        except Error as e:
            print(f"❌ Error al conectar con la base de datos: {e}")
            return None

    def cerrar(self, conn):
        if conn and conn.is_connected():
            conn.close()

    # LOGIN (opcional)
    def login_usuario(self, nombre_usuario, clave):
        conn = self.conectar()
        if not conn:
            return {"status": False, "mensaje": "Error al conectar"}
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT * FROM usuarios WHERE nombre_usuario=%s AND hashed_pass=%s", (nombre_usuario, clave))
            u = cur.fetchone()
            cur.close()
            return {"status": True, "data": u} if u else {"status": False}
        except Exception as e:
            print("Error login:", e)
            return {"status": False, "mensaje": str(e)}
        finally:
            self.cerrar(conn)

    # CONTACTOS (CRUD)
    def get_contactos(self):
        conn = self.conectar()
        if not conn:
            return []
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT ID_contacto, nombre, correo, telefono, asunto, mensaje, fecha_envio, estado, origen, prioridad
                FROM contacto
                ORDER BY ID_contacto DESC
            """)
            rows = cur.fetchall()
            cur.close()
            return rows
        except Exception as e:
            print("Error get_contactos:", e)
            return []
        finally:
            self.cerrar(conn)

    def add_contacto(self, nombre, correo, telefono, asunto, mensaje, fecha_envio, estado, origen, prioridad):
        conn = self.conectar()
        if not conn:
            return False, "Error de conexión"
        try:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO contacto (nombre, correo, telefono, asunto, mensaje, fecha_envio, estado, origen, prioridad)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """, (nombre, correo, telefono, asunto, mensaje, fecha_envio, estado, origen, prioridad))
            conn.commit()
            cur.close()
            return True, None
        except Exception as e:
            conn.rollback()
            print("Error add_contacto:", e)
            return False, str(e)
        finally:
            self.cerrar(conn)

    def update_contacto(self, id_contacto, nombre, correo, telefono, asunto, mensaje, fecha_envio, estado, origen, prioridad):
        conn = self.conectar()
        if not conn:
            return False, "Error de conexión"
        try:
            cur = conn.cursor()
            cur.execute("""
                UPDATE contacto
                SET nombre=%s, correo=%s, telefono=%s, asunto=%s, mensaje=%s,
                    fecha_envio=%s, estado=%s, origen=%s, prioridad=%s
                WHERE ID_contacto=%s
            """, (nombre, correo, telefono, asunto, mensaje, fecha_envio, estado, origen, prioridad, id_contacto))
            conn.commit()
            cur.close()
            return True, None
        except Exception as e:
            conn.rollback()
            print("Error update_contacto:", e)
            return False, str(e)
        finally:
            self.cerrar(conn)

    def delete_contacto(self, id_contacto):
        conn = self.conectar()
        if not conn:
            return False, "Error de conexión"
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM contacto WHERE ID_contacto=%s", (id_contacto,))
            conn.commit()
            cur.close()
            return True, None
        except Exception as e:
            conn.rollback()
            print("Error delete_contacto:", e)
            return False, str(e)
        finally:
            self.cerrar(conn)
