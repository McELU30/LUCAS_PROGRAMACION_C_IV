
import flet as ft
from conexion import ConexionDB

class DocentesView(ft.Container):
    def __init__(self, page, volver_atras):
        super().__init__(expand=True)
        self.page = page
        self.volver_atras = volver_atras
        self.conexion = ConexionDB()

        self.titulo = ft.Text("👨‍🏫 Gestión de Docentes", size=22, weight="bold")

        # Tabla de docentes
        self.tabla = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Código Docente")),
                ft.DataColumn(ft.Text("Nombres")),
                ft.DataColumn(ft.Text("Apellidos")),
                ft.DataColumn(ft.Text("Especialidad")),
                ft.DataColumn(ft.Text("Activo")),
            ],
            rows=[]
        )

        # Botones
        self.btn_volver = ft.ElevatedButton("⬅️ Volver", on_click=lambda e: self.volver_atras())
        self.btn_actualizar = ft.ElevatedButton("🔄 Actualizar", on_click=lambda e: self.cargar_docentes())

        # Layout principal
        self.content = ft.Column(
            [
                self.titulo,
                ft.Row([self.btn_volver, self.btn_actualizar], alignment=ft.MainAxisAlignment.START),
                ft.Container(self.tabla, expand=True, border_radius=10, padding=10, bgcolor=ft.Colors.BLUE_50)
            ],
            spacing=15,
            expand=True,
            scroll=ft.ScrollMode.AUTO
        )

        self.content.visible = True
        self.controls = [self.content]

        # Cargar datos al iniciar
        self.cargar_docentes()

    def cargar_docentes(self):
        conexion = self.conexion.conectar()
        if conexion:
            cursor = conexion.cursor()
            try:
                query = """
                SELECT 
                    d.docente_id,
                    d.codigo_docente,
                    p.nombres,
                    p.apellidos,
                    e.nombre AS especialidad,
                    d.activo
                FROM docentes d
                LEFT JOIN personas p ON d.persona_id = p.persona_id
                LEFT JOIN especialidades e ON d.especialidad_id = e.especialidad_id
                """
                cursor.execute(query)
                resultados = cursor.fetchall()

                self.tabla.rows.clear()
                for fila in resultados:
                    self.tabla.rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(str(fila[0]))),
                                ft.DataCell(ft.Text(fila[1] or "")),
                                ft.DataCell(ft.Text(fila[2] or "")),
                                ft.DataCell(ft.Text(fila[3] or "")),
                                ft.DataCell(ft.Text(fila[4] or "Sin especialidad")),
                                ft.DataCell(ft.Text("Sí" if fila[5] else "No")),
                            ]
                        )
                    )
                self.page.update()

            except Exception as e:
                print(f"❌ Error al cargar docentes: {e}")
            finally:
                self.conexion.cerrar(conexion)
