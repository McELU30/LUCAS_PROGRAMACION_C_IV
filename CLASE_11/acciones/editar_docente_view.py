import flet as ft
from conexion import ConexionDB

class EditarDocenteView(ft.Container):
    def __init__(self, page, docente_id):
        super().__init__(expand=True)
        self.page = page
        self.docente_id = docente_id
        self.conexion = ConexionDB()

        # 🔹 Título
        self.titulo = ft.Text(f"✏️ Editar Docente (ID: {docente_id})", size=22, weight="bold")

        # Contenido mientras carga
        self.column = ft.Column(
            [
                self.titulo,
                ft.ProgressRing(),
            ],
            alignment=ft.MainAxisAlignment.CENTER,   # 🔹 Centra verticalmente
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # 🔹 Centra horizontalmente
            spacing=20,
        )

        # Contenedor principal centrado
        self.content = ft.Container(
            content=self.column,
            alignment=ft.alignment.center,  # 🔹 Asegura el centrado total
            padding=20
        )

        # Mostrar el contenedor
        self.controls = [self.content]
        self.cargar_datos_docente()

    # ───────────────────────────────
    def cargar_datos_docente(self):
        conexion = self.conexion.conectar()
        if conexion:
            cur = conexion.cursor()
            try:
                cur.execute("""
                    SELECT persona_id, codigo_docente, activo, especialidad_id
                    FROM docentes
                    WHERE docente_id = %s
                """, (self.docente_id,))
                datos = cur.fetchone()

                if datos:
                    persona_id, codigo_docente, activo, especialidad_id = datos

                    self.txt_persona = ft.TextField(label="ID Persona", value=str(persona_id), width=350)
                    self.txt_codigo = ft.TextField(label="Código Docente", value=codigo_docente, width=350)
                    self.txt_activo = ft.TextField(label="Activo (1 o 0)", value=str(activo), width=350)
                    self.txt_especialidad = ft.TextField(label="ID Especialidad", value=str(especialidad_id), width=350)

                    btn_guardar = ft.ElevatedButton(
                        "💾 Guardar cambios",
                        bgcolor=ft.Colors.GREEN,
                        color="white",
                        on_click=self.guardar_cambios
                    )

                    btn_atras = ft.OutlinedButton("⬅️ Volver", on_click=self.volver_a_docentes)

                    # 🔹 Reemplazamos el contenido por el formulario centrado
                    self.column.controls.clear()
                    self.column.controls.extend([
                        self.titulo,
                        ft.Column(
                            [
                                self.txt_persona,
                                self.txt_codigo,
                                self.txt_activo,
                                self.txt_especialidad,
                            ],
                            spacing=10,
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER
                        ),
                        ft.Row([btn_guardar, btn_atras], alignment=ft.MainAxisAlignment.CENTER, spacing=15)
                    ])
                    self.page.update()
                else:
                    self.column.controls.clear()
                    self.column.controls.append(ft.Text("❌ No se encontraron datos para este docente.", color="red"))
                    self.page.update()

            except Exception as e:
                print(f"❌ Error al cargar docente: {e}")
            finally:
                self.conexion.cerrar(conexion)

    # ───────────────────────────────
    def guardar_cambios(self, e):
        conexion = self.conexion.conectar()
        if conexion:
            cur = conexion.cursor()
            try:
                cur.execute("""
                    UPDATE docentes
                    SET persona_id=%s, codigo_docente=%s, activo=%s, especialidad_id=%s
                    WHERE docente_id=%s
                """, (
                    self.txt_persona.value,
                    self.txt_codigo.value,
                    self.txt_activo.value,
                    self.txt_especialidad.value,
                    self.docente_id
                ))
                conexion.commit()
                print(f"✅ Docente actualizado correctamente (ID: {self.docente_id})")

                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text("Cambios guardados correctamente ✅", color="white"),
                    bgcolor="green",
                    open=True
                )
                self.page.update()

                self.volver_a_docentes()

            except Exception as ex:
                print(f"❌ Error al guardar cambios: {ex}")
            finally:
                self.conexion.cerrar(conexion)

    # ───────────────────────────────
    def volver_a_docentes(self, e=None):
        """Regresa a la vista principal de docentes."""
        print("🔙 Volviendo a la vista de Docentes...")
        from Docente.docentes_view import DocentesView
        self.page.clean()
        self.page.add(DocentesView(self.page, None))
        self.page.update()