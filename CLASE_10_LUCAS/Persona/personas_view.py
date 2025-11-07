# personas_view.py
import flet as ft
from conexion import ConexionDB
from acciones.editar_persona_view import EditarPersonaView

class PersonasView(ft.Container):
    def __init__(self, page, volver_atras):
        super().__init__(expand=True)
        self.page = page
        self.volver_atras = volver_atras
        self.conexion = ConexionDB()

        self.titulo = ft.Text("👥 Gestión de Personas", size=22, weight="bold")

        # --- Tabla principal ---
        self.tabla = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Nombres")),
                ft.DataColumn(ft.Text("Apellidos")),
                ft.DataColumn(ft.Text("DNI")),
                ft.DataColumn(ft.Text("Teléfono")),
                ft.DataColumn(ft.Text("Acciones")),
            ],
            rows=[]
        )

        # --- Botones superiores ---
        self.btn_volver = ft.ElevatedButton("⬅️ Volver", on_click=lambda e: self.volver_atras())
        self.btn_actualizar = ft.ElevatedButton("🔄 Actualizar", on_click=lambda e: self.cargar_personas())
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

        # --- Cargar datos iniciales ---
        self.cargar_personas()

    # =============================
    #   CARGAR PERSONAS
    # =============================
    def cargar_personas(self):
        print("DEBUG: cargar_personas() start")
        conexion = self.conexion.conectar()
        if conexion:
            cursor = conexion.cursor()
            try:
                cursor.execute("SELECT persona_id, nombres, apellidos, numero_documento, telefono FROM personas")
                resultados = cursor.fetchall()

                self.tabla.rows.clear()
                for fila in resultados:
                    persona_id = fila[0]

                    # --- crear botones fijando el id ---
                    def crear_botones(pid):
                        return ft.Row(
                            [
                                ft.IconButton(
                                    icon=ft.Icons.EDIT,
                                    tooltip="Editar",
                                    on_click=lambda e, _pid=pid: self.mostrar_id_capturado(_pid, "editar")
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.DELETE,
                                    tooltip="Eliminar",
                                    icon_color="red",
                                    on_click=lambda e, _pid=pid: self.mostrar_id_capturado(_pid, "eliminar")
                                )
                            ]
                        )

                    self.tabla.rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(str(persona_id))),
                                ft.DataCell(ft.Text(fila[1] or "")),
                                ft.DataCell(ft.Text(fila[2] or "")),
                                ft.DataCell(ft.Text(fila[3] or "")),
                                ft.DataCell(ft.Text(fila[4] or "")),
                                ft.DataCell(crear_botones(persona_id))
                            ]
                        )
                    )
                self.page.update()
                print("DEBUG: cargar_personas() end - filas cargadas:", len(self.tabla.rows))

            except Exception as e:
                print(f"❌ Error al cargar personas: {e}")
            finally:
                self.conexion.cerrar(conexion)
        else:
            print("DEBUG: cargar_personas() - no hay conexion")

    # =============================
    #   MOSTRAR ID CAPTURADO
    # =============================
    def mostrar_id_capturado(self, persona_id, accion):
        # Depuración inmediata
        print(f"✅ mostrar_id_capturado called -> accion={accion}, id={persona_id}")

        # Mostrar snackbar
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(f"ID capturado para {accion.upper()}: {persona_id}", color="white"),
            bgcolor="green",
            open=True,
            duration=1500
        )
        self.page.update()

        # Ejecutar la acción pedida
        if accion == "editar":
            # Abrimos el formulario de edición
            self.mostrar_formulario_editar(persona_id)
        elif accion == "eliminar":
            # Abrimos confirmación para eliminar
            self.eliminar_persona(persona_id)

    # =============================
    #   FORMULARIO NUEVA PERSONA
    # =============================
    def mostrar_formulario_nuevo(self):
        print("DEBUG: mostrar_formulario_nuevo()")
        txt_nombre = ft.TextField(label="Nombres")
        txt_apellido = ft.TextField(label="Apellidos")
        txt_dni = ft.TextField(label="DNI")
        txt_telefono = ft.TextField(label="Teléfono")

        def guardar_nueva(e):
            print("DEBUG: guardar_nueva()")
            conexion = self.conexion.conectar()
            if conexion:
                cur = conexion.cursor()
                try:
                    cur.execute("""
                        INSERT INTO personas (nombres, apellidos, numero_documento, telefono)
                        VALUES (%s, %s, %s, %s)
                    """, (txt_nombre.value, txt_apellido.value, txt_dni.value, txt_telefono.value))
                    conexion.commit()
                    print("DEBUG: Persona insertada, recargando tabla")
                    self.cerrar_dialogo(dlg)
                    self.cargar_personas()
                except Exception as ex:
                    print(f"❌ Error al insertar persona: {ex}")
                finally:
                    self.conexion.cerrar(conexion)

        dlg = ft.AlertDialog(
            title=ft.Text("➕ Nueva Persona"),
            content=ft.Column([txt_nombre, txt_apellido, txt_dni, txt_telefono], spacing=10),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.cerrar_dialogo(dlg)),
                ft.TextButton("Guardar", on_click=guardar_nueva),
            ]
        )
        # Abrir diálogo de forma explícita
        self.page.show_dialog(dlg)

    # =============================
    #   FORMULARIO EDITAR PERSONA
    # =============================
    def mostrar_formulario_editar(self, persona_id):
        print(f"🧩 Abriendo ventana de edición para persona {persona_id}")
        from acciones.editar_persona_view import EditarPersonaView

        # Crear la vista de edición sin usar volver_atras
        editar_vista = EditarPersonaView(self.page, None, persona_id)

        # Mostramos directamente la vista de edición en la página
        self.page.controls.clear()
        self.page.add(editar_vista)
        self.page.update()
        
    def mostrar_formulario_editar(self, persona_id):
        print(f"🧩 Navegando a vista de edición para persona {persona_id}")
        from acciones.editar_persona_view import EditarPersonaView
        editar_vista = EditarPersonaView(self.page, persona_id)
        self.page.clean()
        self.page.add(editar_vista)

    # =============================
    #   ELIMINAR PERSONA
    # =============================
    def eliminar_persona(self, persona_id):
        print(f"DEBUG: eliminar_persona({persona_id}) -> abrir confirm")
        dlg_confirm = ft.AlertDialog(
            title=ft.Text("⚠️ Confirmar eliminación"),
            content=ft.Text("¿Está seguro de que desea eliminar esta persona?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.cerrar_dialogo(dlg_confirm)),
                ft.TextButton(
                    "Eliminar",
                    style=ft.ButtonStyle(color="white", bgcolor="red"),
                    on_click=lambda e: self.confirmar_eliminar(persona_id, dlg_confirm)
                )
            ]
        )
        self.page.dialog = dlg_confirm
        self.page.dialog.open = True
        self.page.update()

    def confirmar_eliminar(self, persona_id, dlg_confirm):
        print(f"DEBUG: confirmar_eliminar({persona_id})")
        conexion = self.conexion.conectar()
        if conexion:
            cursor = conexion.cursor()
            try:
                cursor.execute("DELETE FROM personas WHERE persona_id = %s", (persona_id,))
                conexion.commit()
                print("DEBUG: Persona eliminada, recargando tabla")
                self.cerrar_dialogo(dlg_confirm)
                self.cargar_personas()
            except Exception as e:
                print(f"❌ Error al eliminar persona: {e}")
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
            print("DEBUG: error cerrando dialogo:", e)