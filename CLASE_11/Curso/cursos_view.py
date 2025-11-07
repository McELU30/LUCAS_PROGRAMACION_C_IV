import flet as ft
from conexion import ConexionDB
from acciones.editar_curso_view import EditarCursoView

class CursosView(ft.Container):
    def __init__(self, page, volver_atras):
        super().__init__(expand=True)
        self.page = page
        self.volver_atras = volver_atras
        self.conexion = ConexionDB()

        self.titulo = ft.Text("📚 Gestión de Cursos", size=22, weight="bold")

        # --- Tabla principal ---
        self.tabla = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Código")),
                ft.DataColumn(ft.Text("Nombre")),
                ft.DataColumn(ft.Text("Créditos")),
                ft.DataColumn(ft.Text("Horas")),
                ft.DataColumn(ft.Text("Descripción")),
                ft.DataColumn(ft.Text("Acciones")),
            ],
            rows=[]
        )

        # --- Botones superiores ---
        self.btn_volver = ft.ElevatedButton("⬅️ Volver", on_click=lambda e: self.volver_atras())
        self.btn_actualizar = ft.ElevatedButton("🔄 Actualizar", on_click=lambda e: self.cargar_cursos())
        self.btn_agregar = ft.ElevatedButton("➕ Agregar", on_click=lambda e: self.mostrar_formulario_nuevo())

        # --- Contenedor principal ---
        self.content = ft.Column(
            [
                self.titulo,
                ft.Row([self.btn_volver, self.btn_actualizar, self.btn_agregar], alignment=ft.MainAxisAlignment.START),
                ft.Container(self.tabla, expand=True, border_radius=10, padding=10, bgcolor=ft.Colors.BLUE_50)
            ],
            spacing=15,
            expand=True,
            scroll=ft.ScrollMode.AUTO
        )

        self.controls = [self.content]
        self.cargar_cursos()

    # =============================
    #   CARGAR CURSOS
    # =============================
    def cargar_cursos(self):
        print("DEBUG: cargar_cursos() start")
        conexion = self.conexion.conectar()
        if conexion:
            cursor = conexion.cursor()
            try:
                cursor.execute("SELECT curso_id, codigo, nombre, creditos, horas, descripcion FROM cursos")
                resultados = cursor.fetchall()

                self.tabla.rows.clear()
                for fila in resultados:
                    curso_id = fila[0]

                    def crear_botones(cid):
                        return ft.Row(
                            [
                                ft.IconButton(
                                    icon=ft.Icons.EDIT,
                                    tooltip="Editar",
                                    on_click=lambda e, _cid=cid: self.mostrar_id_capturado(_cid, "editar")
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.DELETE,
                                    tooltip="Eliminar",
                                    icon_color="red",
                                    on_click=lambda e, _cid=cid: self.mostrar_id_capturado(_cid, "eliminar")
                                )
                            ]
                        )

                    self.tabla.rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(str(curso_id))),
                                ft.DataCell(ft.Text(fila[1] or "")),
                                ft.DataCell(ft.Text(fila[2] or "")),
                                ft.DataCell(ft.Text(str(fila[3]) if fila[3] is not None else "")),
                                ft.DataCell(ft.Text(str(fila[4]) if fila[4] is not None else "")),
                                ft.DataCell(ft.Text(fila[5] or "")),
                                ft.DataCell(crear_botones(curso_id))
                            ]
                        )
                    )
                self.page.update()
                print("DEBUG: cargar_cursos() end - filas cargadas:", len(self.tabla.rows))

            except Exception as e:
                print(f"❌ Error al cargar cursos: {e}")
            finally:
                self.conexion.cerrar(conexion)
        else:
            print("DEBUG: cargar_cursos() - no hay conexión")

    # =============================
    #   MOSTRAR ID CAPTURADO
    # =============================
    def mostrar_id_capturado(self, curso_id, accion):
        print(f"✅ mostrar_id_capturado -> accion={accion}, id={curso_id}")

        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(f"ID capturado para {accion.upper()}: {curso_id}", color="white"),
            bgcolor="green",
            open=True,
            duration=1500
        )
        self.page.update()

        if accion == "editar":
            self.mostrar_formulario_editar(curso_id)
        elif accion == "eliminar":
            self.eliminar_curso(curso_id)

    # =============================
    #   FORMULARIO NUEVO CURSO
    # =============================
    def mostrar_formulario_nuevo(self):
        print("DEBUG: mostrar_formulario_nuevo()")
        txt_codigo = ft.TextField(label="Código del curso")
        txt_nombre = ft.TextField(label="Nombre del curso")
        txt_creditos = ft.TextField(label="Créditos", keyboard_type=ft.KeyboardType.NUMBER)
        txt_horas = ft.TextField(label="Horas", keyboard_type=ft.KeyboardType.NUMBER)
        txt_descripcion = ft.TextField(label="Descripción", multiline=True)

        def guardar_nuevo(e):
            print("DEBUG: guardar_nuevo()")
            conexion = self.conexion.conectar()
            if conexion:
                cur = conexion.cursor()
                try:
                    cur.execute("""
                        INSERT INTO cursos (codigo, nombre, creditos, horas, descripcion, creado_en)
                        VALUES (%s, %s, %s, %s, %s, NOW())
                    """, (txt_codigo.value, txt_nombre.value, txt_creditos.value, txt_horas.value, txt_descripcion.value))
                    conexion.commit()
                    print("✅ Curso insertado correctamente")
                    self.cerrar_dialogo(dlg)
                    self.cargar_cursos()
                except Exception as ex:
                    print(f"❌ Error al insertar curso: {ex}")
                finally:
                    self.conexion.cerrar(conexion)

        dlg = ft.AlertDialog(
            title=ft.Text("➕ Nuevo Curso"),
            content=ft.Column([txt_codigo, txt_nombre, txt_creditos, txt_horas, txt_descripcion], spacing=10),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.cerrar_dialogo(dlg)),
                ft.TextButton("Guardar", on_click=guardar_nuevo),
            ]
        )
        self.page.show_dialog(dlg)

    # =============================
    #   FORMULARIO EDITAR CURSO
    # =============================
    def mostrar_formulario_editar(self, curso_id):
        print(f"🧩 Navegando a vista de edición para curso {curso_id}")
        editar_vista = EditarCursoView(self.page, curso_id)
        self.page.clean()
        self.page.add(editar_vista)

    # =============================
    #   ELIMINAR CURSO
    # =============================
    def eliminar_curso(self, curso_id):
        print(f"DEBUG: eliminar_curso({curso_id}) -> abrir confirmación")
        dlg_confirm = ft.AlertDialog(
            title=ft.Text("⚠️ Confirmar eliminación"),
            content=ft.Text("¿Está seguro de que desea eliminar este curso?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.cerrar_dialogo(dlg_confirm)),
                ft.TextButton(
                    "Eliminar",
                    style=ft.ButtonStyle(color="white", bgcolor="red"),
                    on_click=lambda e: self.confirmar_eliminar(curso_id, dlg_confirm)
                )
            ]
        )
        self.page.dialog = dlg_confirm
        self.page.dialog.open = True
        self.page.update()

    def confirmar_eliminar(self, curso_id, dlg_confirm):
        print(f"DEBUG: confirmar_eliminar({curso_id})")
        conexion = self.conexion.conectar()
        if conexion:
            cursor = conexion.cursor()
            try:
                cursor.execute("DELETE FROM cursos WHERE curso_id = %s", (curso_id,))
                conexion.commit()
                print("✅ Curso eliminado correctamente")
                self.cerrar_dialogo(dlg_confirm)
                self.cargar_cursos()
            except Exception as e:
                print(f"❌ Error al eliminar curso: {e}")
            finally:
                self.conexion.cerrar(conexion)

    # =============================
    #   CERRAR DIÁLOGO
    # =============================
    def cerrar_dialogo(self, dlg):
        try:
            dlg.open = False
            self.page.update()
        except Exception as e:
            print("DEBUG: error cerrando diálogo:", e)
 