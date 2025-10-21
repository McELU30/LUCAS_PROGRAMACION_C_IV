import flet as ft
from conexion import ConexionDB

class UsuariosView(ft.Container):
    def __init__(self, page, volver_atras):
        super().__init__(expand=True)
        self.page = page
        self.volver_atras = volver_atras
        self.conexion = ConexionDB()

        # Título
        self.titulo = ft.Text("👤 Gestión de Usuarios", size=22, weight="bold")

        # Tabla de usuarios
        self.tabla = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Persona ID")),
                ft.DataColumn(ft.Text("Nombre de usuario")),
                ft.DataColumn(ft.Text("Email")),
                ft.DataColumn(ft.Text("Rol")),
                ft.DataColumn(ft.Text("Activo")),
                ft.DataColumn(ft.Text("Último login")),
                ft.DataColumn(ft.Text("Creado en")),
            ],
            rows=[]
        )

        # Botones
        self.btn_volver = ft.ElevatedButton("⬅️ Volver", on_click=lambda e: self.volver_atras())
        self.btn_actualizar = ft.ElevatedButton("🔄 Actualizar", on_click=lambda e: self.cargar_usuarios())

        # Layout principal
        self.content = ft.Column(
            [
                self.titulo,
                ft.Row([self.btn_volver, self.btn_actualizar], alignment=ft.MainAxisAlignment.START),
                ft.Container(
                    self.tabla,
                    expand=True,
                    border_radius=10,
                    padding=10,
                    bgcolor=ft.Colors.BLUE_50
                ),
            ],
            spacing=15,
            expand=True,
            scroll=ft.ScrollMode.AUTO
        )

        self.content.visible = True
        self.controls = [self.content]

        # Cargar datos al iniciar
        self.cargar_usuarios()

    def cargar_usuarios(self):
        conexion = self.conexion.conectar()
        if conexion:
            cursor = conexion.cursor()
            try:
                query = """
                SELECT 
                    usuario_id,
                    persona_id,
                    nombre_usuario,
                    usuariosemail,
                    rol,
                    activo,
                    ultimo_login,
                    creado_en
                FROM usuarios
                """
                cursor.execute(query)
                resultados = cursor.fetchall()

                self.tabla.rows.clear()
                for fila in resultados:
                    self.tabla.rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(str(fila[0]))),   # usuario_id
                                ft.DataCell(ft.Text(str(fila[1]) if fila[1] else "-")),  # persona_id
                                ft.DataCell(ft.Text(fila[2] or "")),  # nombre_usuario
                                ft.DataCell(ft.Text(fila[3] or "")),  # usuariosemail
                                ft.DataCell(ft.Text(fila[4] or "")),  # rol
                                ft.DataCell(ft.Text("Sí" if fila[5] else "No")),  # activo
                                ft.DataCell(ft.Text(str(fila[6]) if fila[6] else "-")),  # ultimo_login
                                ft.DataCell(ft.Text(str(fila[7]) if fila[7] else "-")),  # creado_en
                            ]
                        )
                    )
                self.page.update()

            except Exception as e:
                print(f"❌ Error al cargar usuarios: {e}")
            finally:
                self.conexion.cerrar(conexion)
