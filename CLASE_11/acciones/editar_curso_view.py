import flet as ft
from conexion import ConexionDB

class EditarCursoView(ft.Container):
    def __init__(self, page, id_curso):
        super().__init__(expand=True)
        self.page = page
        self.id_curso = id_curso
        self.conexion = ConexionDB()

        self.titulo = ft.Text(f"✏️ Editar Curso (ID: {id_curso})", size=22, weight="bold")

        # Contenido temporal mientras carga
        self.column = ft.Column(
            [
                self.titulo,
                ft.ProgressRing(),
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        )

        self.content = ft.Container(
            content=self.column,
            alignment=ft.alignment.center,
            padding=20
        )

        self.cargar_datos_curso()

    # ───────────────────────────────
    def cargar_datos_curso(self):
        conexion = self.conexion.conectar()
        if conexion:
            cur = conexion.cursor()
            try:
                cur.execute("""
                    SELECT codigo, nombre, creditos, horas, descripcion
                    FROM cursos
                    WHERE curso_id = %s
                """, (self.id_curso,))
                datos = cur.fetchone()

                if datos:
                    codigo, nombre, creditos, horas, descripcion = datos

                    # Campos dinámicos
                    self.txt_codigo = ft.TextField(label="Código del Curso", value=codigo, width=400)
                    self.txt_nombre = ft.TextField(label="Nombre del Curso", value=nombre, width=400)
                    self.txt_creditos = ft.TextField(
                        label="Créditos",
                        value=str(creditos),
                        width=400,
                        keyboard_type=ft.KeyboardType.NUMBER
                    )
                    self.txt_horas = ft.TextField(
                        label="Horas",
                        value=str(horas),
                        width=400,
                        keyboard_type=ft.KeyboardType.NUMBER
                    )
                    self.txt_descripcion = ft.TextField(
                        label="Descripción",
                        value=descripcion,
                        multiline=True,
                        width=400
                    )

                    btn_guardar = ft.ElevatedButton(
                        "💾 Guardar cambios",
                        bgcolor=ft.Colors.GREEN,
                        color="white",
                        on_click=self.guardar_cambios
                    )

                    btn_atras = ft.OutlinedButton(
                        "⬅️ Volver a lista",
                        on_click=self.volver_a_cursos
                    )

                    # Actualizamos el contenido
                    self.column.controls.clear()
                    self.column.controls.extend([
                        self.titulo,
                        ft.Column(
                            [
                                self.txt_codigo,
                                self.txt_nombre,
                                self.txt_creditos,
                                self.txt_horas,
                                self.txt_descripcion
                            ],
                            spacing=10
                        ),
                        ft.Row([btn_guardar, btn_atras], spacing=15)
                    ])
                    self.page.update()
                else:
                    self.column.controls.clear()
                    self.column.controls.append(ft.Text("❌ No se encontraron datos para este curso.", color="red"))
                    self.page.update()

            except Exception as e:
                print(f"❌ Error al cargar curso: {e}")
            finally:
                self.conexion.cerrar(conexion)

    # ───────────────────────────────
    def guardar_cambios(self, e):
        conexion = self.conexion.conectar()
        if conexion:
            cur = conexion.cursor()
            try:
                cur.execute("""
                    UPDATE cursos
                    SET codigo=%s, nombre=%s, creditos=%s, horas=%s, descripcion=%s, actualizado_en=NOW()
                    WHERE curso_id=%s
                """, (
                    self.txt_codigo.value,
                    self.txt_nombre.value,
                    self.txt_creditos.value,
                    self.txt_horas.value,
                    self.txt_descripcion.value,
                    self.id_curso
                ))
                conexion.commit()

                print(f"✅ Curso actualizado correctamente (ID: {self.id_curso})")

                self.page.snack_bar = ft.SnackBar(
                    ft.Text("Cambios guardados correctamente ✅", color="white"),
                    bgcolor="green",
                    open=True
                )
                self.page.update()

                # Volvemos a la lista automáticamente después de guardar
                self.volver_a_cursos()

            except Exception as ex:
                print(f"❌ Error al guardar cambios: {ex}")
            finally:
                self.conexion.cerrar(conexion)

    # ───────────────────────────────
    def volver_a_cursos(self, e=None):
        """Regresa a la vista de Cursos."""
        print("🔙 Volviendo a la vista de Cursos...")
        from Curso.cursos_view import CursosView

        self.page.clean()
        self.page.add(CursosView(self.page, None))
        self.page.update()