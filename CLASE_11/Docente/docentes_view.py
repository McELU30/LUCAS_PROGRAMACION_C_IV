import flet as ft
from conexion import ConexionDB
from acciones.editar_docente_view import EditarDocenteView

class DocentesView(ft.Container):
    def __init__(self, page, volver_atras):
        super().__init__(expand=True)
        self.page = page
        self.volver_atras = volver_atras
        self.conexion = ConexionDB()

        # 🔹 Título principal
        self.titulo = ft.Text("👨‍🏫 Gestión de Docentes", size=22, weight="bold")

        # 🔹 Tabla de docentes
        self.tabla = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Persona ID")),
                ft.DataColumn(ft.Text("Código Docente")),
                ft.DataColumn(ft.Text("Activo")),
                ft.DataColumn(ft.Text("Especialidad ID")),
                ft.DataColumn(ft.Text("Acciones")),
            ],
            rows=[]
        )

        # 🔹 Botones superiores
        self.btn_volver = ft.ElevatedButton("⬅️ Volver", on_click=lambda e: self.volver_atras())
        self.btn_actualizar = ft.ElevatedButton("🔄 Actualizar", on_click=lambda e: self.cargar_docentes())
        self.btn_agregar = ft.ElevatedButton("➕ Agregar", on_click=lambda e: self.mostrar_formulario_nuevo())

        # 🔹 Estructura general
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

        # Cargar datos iniciales
        self.cargar_docentes()

    # =============================
    #   CARGAR DOCENTES
    # =============================
    def cargar_docentes(self):
        conexion = self.conexion.conectar()
        if conexion:
            cursor = conexion.cursor()
            try:
                cursor.execute("""
                    SELECT docente_id, persona_id, codigo_docente, activo, especialidad_id
                    FROM docentes
                """)
                resultados = cursor.fetchall()

                self.tabla.rows.clear()
                for fila in resultados:
                    docente_id = fila[0]

                    # Botones de acción
                    def crear_botones(did):
                        return ft.Row(
                            [
                                ft.IconButton(
                                    icon=ft.Icons.EDIT,
                                    tooltip="Editar",
                                    on_click=lambda e, _did=did: self.mostrar_id_capturado(_did, "editar")
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.DELETE,
                                    tooltip="Eliminar",
                                    icon_color="red",
                                    on_click=lambda e, _did=did: self.mostrar_id_capturado(_did, "eliminar")
                                )
                            ]
                        )

                    self.tabla.rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(str(fila[0]))),
                                ft.DataCell(ft.Text(str(fila[1]))),
                                ft.DataCell(ft.Text(fila[2] or "")),
                                ft.DataCell(ft.Text("Sí" if fila[3] else "No")),
                                ft.DataCell(ft.Text(str(fila[4]) if fila[4] else "")),
                                ft.DataCell(crear_botones(docente_id))
                            ]
                        )
                    )
                self.page.update()
                print("✅ Datos de docentes cargados correctamente")

            except Exception as e:
                print(f"❌ Error al cargar docentes: {e}")
            finally:
                self.conexion.cerrar(conexion)

    # =============================
    #   CAPTURAR ID Y ACCIÓN
    # =============================
    def mostrar_id_capturado(self, docente_id, accion):
        print(f"🧩 Acción: {accion}, ID: {docente_id}")
        self.page.snack_bar = ft.SnackBar(
            ft.Text(f"Docente ID {docente_id} - Acción: {accion.upper()}", color="white"),
            bgcolor="green",
            open=True,
            duration=1500
        )
        self.page.update()

        if accion == "editar":
            self.mostrar_formulario_editar(docente_id)
        elif accion == "eliminar":
            self.eliminar_docente(docente_id)

    # =============================
    #   FORMULARIO NUEVO DOCENTE
    # =============================
    def mostrar_formulario_nuevo(self):
        txt_persona_id = ft.TextField(label="Persona ID")
        txt_codigo = ft.TextField(label="Código Docente")
        txt_activo = ft.Switch(label="Activo", value=True)
        txt_especialidad = ft.TextField(label="Especialidad ID")

        def guardar_nuevo(e):
            conexion = self.conexion.conectar()
            if conexion:
                cur = conexion.cursor()
                try:
                    cur.execute("""
                        INSERT INTO docentes (persona_id, codigo_docente, activo, especialidad_id)
                        VALUES (%s, %s, %s, %s)
                    """, (
                        txt_persona_id.value,
                        txt_codigo.value,
                        txt_activo.value,
                        txt_especialidad.value
                    ))
                    conexion.commit()
                    self.cerrar_dialogo(dlg)
                    self.cargar_docentes()
                except Exception as ex:
                    print(f"❌ Error al insertar docente: {ex}")
                finally:
                    self.conexion.cerrar(conexion)

        dlg = ft.AlertDialog(
            title=ft.Text("➕ Nuevo Docente"),
            content=ft.Column([txt_persona_id, txt_codigo, txt_activo, txt_especialidad], spacing=10),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.cerrar_dialogo(dlg)),
                ft.TextButton("Guardar", on_click=guardar_nuevo),
            ]
        )
        self.page.show_dialog(dlg)

    # =============================
    #   FORMULARIO EDITAR DOCENTE
    # =============================
    def mostrar_formulario_editar(self, docente_id):
        print(f"🧩 Abriendo edición para docente {docente_id}")
        editar_vista = EditarDocenteView(self.page, docente_id)
        self.page.clean()
        self.page.add(editar_vista)
        self.page.update()

    # =============================
    #   ELIMINAR DOCENTE
    # =============================
    def eliminar_docente(self, docente_id):
        dlg_confirm = ft.AlertDialog(
            title=ft.Text("⚠️ Confirmar eliminación"),
            content=ft.Text("¿Está seguro de eliminar este docente?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.cerrar_dialogo(dlg_confirm)),
                ft.TextButton(
                    "Eliminar",
                    style=ft.ButtonStyle(color="white", bgcolor="red"),
                    on_click=lambda e: self.confirmar_eliminar(docente_id, dlg_confirm)
                )
            ]
        )
        self.page.dialog = dlg_confirm
        self.page.dialog.open = True
        self.page.update()

    def confirmar_eliminar(self, docente_id, dlg_confirm):
        conexion = self.conexion.conectar()
        if conexion:
            cursor = conexion.cursor()
            try:
                cursor.execute("DELETE FROM docentes WHERE docente_id = %s", (docente_id,))
                conexion.commit()
                self.cerrar_dialogo(dlg_confirm)
                self.cargar_docentes()
            except Exception as e:
                print(f"❌ Error al eliminar docente: {e}")
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
            print("⚠️ Error al cerrar diálogo:", e)