import mysql.connector
from mysql.connector import Error
from conexion import ConexionDB


class CursoModel:
    def __init__(self):
        self.db = ConexionDB()

    # ───────────────────────────────
    def listar_cursos(self):
        """Obtiene todos los cursos registrados."""
        conexion = self.db.conectar()
        if not conexion:
            return []

        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("SELECT * FROM cursos ORDER BY id_curso ASC")
            cursos = cursor.fetchall()
            return cursos
        except Error as e:
            print(f"❌ Error al listar cursos: {e}")
            return []
        finally:
            if 'cursor' in locals():
                cursor.close()
            self.db.cerrar(conexion)

    # ───────────────────────────────
    def obtener_curso(self, id_curso):
        """Obtiene los datos de un curso específico."""
        conexion = self.db.conectar()
        if not conexion:
            return None

        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("SELECT * FROM cursos WHERE id_curso = %s", (id_curso,))
            curso = cursor.fetchone()
            return curso
        except Error as e:
            print(f"❌ Error al obtener curso: {e}")
            return None
        finally:
            if 'cursor' in locals():
                cursor.close()
            self.db.cerrar(conexion)

    # ───────────────────────────────
    def agregar_curso(self, nombre, descripcion, creditos, estado):
        """Agrega un nuevo curso a la base de datos."""
        conexion = self.db.conectar()
        if not conexion:
            return {"status": False, "mensaje": "Error de conexión"}

        try:
            cursor = conexion.cursor()
            cursor.execute("""
                INSERT INTO cursos (nombre, descripcion, creditos, estado)
                VALUES (%s, %s, %s, %s)
            """, (nombre, descripcion, creditos, estado))
            conexion.commit()
            print("✅ Curso agregado correctamente")
            return {"status": True, "mensaje": "Curso registrado correctamente"}
        except Error as e:
            print(f"❌ Error al agregar curso: {e}")
            return {"status": False, "mensaje": str(e)}
        finally:
            if 'cursor' in locals():
                cursor.close()
            self.db.cerrar(conexion)

    # ───────────────────────────────
    def actualizar_curso(self, id_curso, nombre, descripcion, creditos, estado):
        """Actualiza los datos de un curso existente."""
        conexion = self.db.conectar()
        if not conexion:
            return {"status": False, "mensaje": "Error de conexión"}

        try:
            cursor = conexion.cursor()
            cursor.execute("""
                UPDATE cursos
                SET nombre=%s, descripcion=%s, creditos=%s, estado=%s
                WHERE id_curso=%s
            """, (nombre, descripcion, creditos, estado, id_curso))
            conexion.commit()
            print(f"✅ Curso actualizado correctamente (ID: {id_curso})")
            return {"status": True, "mensaje": "Curso actualizado correctamente"}
        except Error as e:
            print(f"❌ Error al actualizar curso: {e}")
            return {"status": False, "mensaje": str(e)}
        finally:
            if 'cursor' in locals():
                cursor.close()
            self.db.cerrar(conexion)

    # ───────────────────────────────
    def eliminar_curso(self, id_curso):
        """Elimina un curso por su ID."""
        conexion = self.db.conectar()
        if not conexion:
            return {"status": False, "mensaje": "Error de conexión"}

        try:
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM cursos WHERE id_curso = %s", (id_curso,))
            conexion.commit()
            print(f"🗑️ Curso eliminado correctamente (ID: {id_curso})")
            return {"status": True, "mensaje": "Curso eliminado correctamente"}
        except Error as e:
            print(f"❌ Error al eliminar curso: {e}")
            return {"status": False, "mensaje": str(e)}
        finally:
            if 'cursor' in locals():
                cursor.close()
            self.db.cerrar(conexion)


# ───────────────────────────────
# 🚀 Prueba directa (debug)
# ───────────────────────────────
if __name__ == "__main__":
    modelo = CursoModel()

    # Ejemplo: agregar curso
    # modelo.agregar_curso("Matemática II", "Curso avanzado de álgebra y trigonometría", 4, "Activo")

    # Ejemplo: listar
    cursos = modelo.listar_cursos()
    for c in cursos:
        print(c)