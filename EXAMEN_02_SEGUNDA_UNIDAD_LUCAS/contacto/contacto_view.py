# contacto/contacto_view.py
import flet as ft
from conexion import ConexionDB
from datetime import datetime
from functools import partial

class ContactoView(ft.Container):
    def __init__(self, page: ft.Page, volver_atras):
        super().__init__(expand=True)
        self.page = page
        self.volver_atras = volver_atras
        self.db = ConexionDB()

        self.titulo = ft.Text("👥 Gestión de Contactos", size=22, weight="bold")
        self.btn_volver = ft.ElevatedButton("⬅️ Volver", on_click=lambda e: self.volver_atras())
        self.btn_agregar = ft.ElevatedButton("➕ Agregar", on_click=lambda e: self.abrir_agregar_dialog())
        self.btn_actualizar = ft.ElevatedButton("🔄 Actualizar", on_click=lambda e: self.cargar_contacto())

        self.tabla = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Nombre")),
                ft.DataColumn(ft.Text("Correo")),
                ft.DataColumn(ft.Text("Teléfono")),
                ft.DataColumn(ft.Text("Asunto")),
                ft.DataColumn(ft.Text("Mensaje")),
                ft.DataColumn(ft.Text("Fecha envío")),
                ft.DataColumn(ft.Text("Estado")),
                ft.DataColumn(ft.Text("Origen")),
                ft.DataColumn(ft.Text("Prioridad")),
                ft.DataColumn(ft.Text("Acciones")),
            ],
            rows=[]
        )

        self.content = ft.Column(
            [
                ft.Row([self.titulo]),
                ft.Row([self.btn_volver, self.btn_agregar, self.btn_actualizar], alignment=ft.MainAxisAlignment.START),
                ft.Container(self.tabla, expand=True, border_radius=10, padding=10, bgcolor=ft.Colors.BLUE_50)
            ],
            spacing=12,
            expand=True,
            scroll=ft.ScrollMode.AUTO
        )

        print("DEBUG: ContactoView inicializado")
        self.cargar_contacto()

    def _close_dialog_if_any(self):
        # Cierra cualquier diálogo abierto (evita que un diálogo invisible bloquee clicks)
        try:
            if getattr(self.page, "dialog", None):
                self.page.dialog.open = False
                self.page.dialog = None
                self.page.update()
        except Exception:
            pass

    def cargar_contacto(self):
        print("DEBUG: cargar_contacto -> solicitando datos")
        self._close_dialog_if_any()
        resultados = self.db.get_contactos()
        print(f"DEBUG: get_contactos devolvió {len(resultados)} filas")
        self.tabla.rows.clear()

        for fila in resultados:
            idc = fila[0]
            nombre = str(fila[1] or "")
            correo = str(fila[2] or "")
            telefono = str(fila[3] or "")
            asunto = str(fila[4] or "")
            mensaje = str(fila[5] or "")
            fecha = str(fila[6] or "")
            estado = str(fila[7] or "")
            origen = str(fila[8] or "")
            prioridad = str(fila[9] or "")

            # Usar partial para ligar el id sin problemas de cierre (closure)
            editar_btn = ft.IconButton(icon=ft.Icons.EDIT, tooltip="Editar", on_click=partial(self._on_click_editar, idc))
            eliminar_btn = ft.IconButton(icon=ft.Icons.DELETE, tooltip="Eliminar", on_click=partial(self._on_click_eliminar, idc))
            acciones = ft.Row([editar_btn, eliminar_btn], spacing=0)

            self.tabla.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(idc))),
                        ft.DataCell(ft.Text(nombre)),
                        ft.DataCell(ft.Text(correo)),
                        ft.DataCell(ft.Text(telefono)),
                        ft.DataCell(ft.Text(asunto)),
                        ft.DataCell(ft.Text(mensaje)),
                        ft.DataCell(ft.Text(fecha)),
                        ft.DataCell(ft.Text(estado)),
                        ft.DataCell(ft.Text(origen)),
                        ft.DataCell(ft.Text(prioridad)),
                        ft.DataCell(acciones),
                    ]
                )
            )

        print("DEBUG: filas añadidas a DataTable:", len(self.tabla.rows))
        self.page.update()

    # ---------- WRAPPERS con DEBUG ----------
    def _on_click_editar(self, id_contacto, e):
        print("DEBUG: editar pulsado para id:", id_contacto)
        # asegurarse de cerrar cualquier diálogo previo
        self._close_dialog_if_any()
        self.abrir_editar_dialog(id_contacto)

    def _on_click_eliminar(self, id_contacto, e):
        print("DEBUG: eliminar pulsado para id:", id_contacto)
        self._close_dialog_if_any()
        self.confirmar_eliminar(id_contacto)

    # ---------- AGREGAR ----------
    def abrir_agregar_dialog(self):
        print("DEBUG: abrir_agregar_dialog")
        tf_nombre = ft.TextField(label="Nombre", width=300)
        tf_correo = ft.TextField(label="Correo", width=300)
        tf_telefono = ft.TextField(label="Teléfono", width=200)
        tf_asunto = ft.TextField(label="Asunto", width=300)
        tf_mensaje = ft.TextField(label="Mensaje", width=400, multiline=True)
        tf_fecha = ft.TextField(label="Fecha envío (YYYY-MM-DD HH:MM:SS)", value=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        tf_estado = ft.TextField(label="Estado", width=150, value="nuevo")
        tf_origen = ft.TextField(label="Origen", width=150, value="web")
        tf_prioridad = ft.TextField(label="Prioridad", width=150, value="media")

        lbl_error = ft.Text("", color=ft.Colors.RED)

        def on_agregar(e):
            print("DEBUG: on_agregar -> guardando nuevo contacto")
            ok, err = self.db.add_contacto(
                tf_nombre.value, tf_correo.value, tf_telefono.value, tf_asunto.value,
                tf_mensaje.value, tf_fecha.value, tf_estado.value, tf_origen.value, tf_prioridad.value
            )
            if ok:
                dialog.open = False
                self.page.dialog = None
                self.cargar_contacto()
            else:
                lbl_error.value = f"Error: {err}"
                dialog.update()

        dialog = ft.AlertDialog(
            title=ft.Text("➕ Agregar Contacto"),
            content=ft.Column([tf_nombre, tf_correo, tf_telefono, tf_asunto, tf_mensaje, tf_fecha, tf_estado, tf_origen, tf_prioridad, lbl_error]),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: (setattr(self.page, "dialog", None), self.page.update())),
                ft.ElevatedButton("Agregar", on_click=on_agregar)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    # ---------- EDITAR ----------
    def abrir_editar_dialog(self, id_contacto):
        print("DEBUG: abrir_editar_dialog para id", id_contacto)
        resultados = self.db.get_contactos()
        registro = None
        for fila in resultados:
            if fila[0] == id_contacto:
                registro = fila
                break
        if not registro:
            print("Registro no encontrado:", id_contacto)
            return

        tf_nombre = ft.TextField(label="Nombre", value=str(registro[1] or ""))
        tf_correo = ft.TextField(label="Correo", value=str(registro[2] or ""))
        tf_telefono = ft.TextField(label="Teléfono", value=str(registro[3] or ""))
        tf_asunto = ft.TextField(label="Asunto", value=str(registro[4] or ""))
        tf_mensaje = ft.TextField(label="Mensaje", value=str(registro[5] or ""), multiline=True)
        tf_fecha = ft.TextField(label="Fecha envío (YYYY-MM-DD HH:MM:SS)", value=str(registro[6] or ""))
        tf_estado = ft.TextField(label="Estado", value=str(registro[7] or ""))
        tf_origen = ft.TextField(label="Origen", value=str(registro[8] or ""))
        tf_prioridad = ft.TextField(label="Prioridad", value=str(registro[9] or ""))

        lbl_error = ft.Text("", color=ft.Colors.RED)

        def on_guardar(e):
            print("DEBUG: on_guardar -> actualizando id", id_contacto)
            ok, err = self.db.update_contacto(
                id_contacto,
                tf_nombre.value, tf_correo.value, tf_telefono.value, tf_asunto.value,
                tf_mensaje.value, tf_fecha.value, tf_estado.value, tf_origen.value, tf_prioridad.value
            )
            if ok:
                dialog.open = False
                self.page.dialog = None
                self.cargar_contacto()
            else:
                lbl_error.value = f"Error: {err}"
                dialog.update()

        dialog = ft.AlertDialog(
            title=ft.Text("✏️ Editar Contacto"),
            content=ft.Column([tf_nombre, tf_correo, tf_telefono, tf_asunto, tf_mensaje, tf_fecha, tf_estado, tf_origen, tf_prioridad, lbl_error]),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: (setattr(self.page, "dialog", None), self.page.update())),
                ft.ElevatedButton("Guardar", on_click=on_guardar)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    # ---------- ELIMINAR ----------
    def confirmar_eliminar(self, id_contacto):
        print("DEBUG: confirmar_eliminar para id", id_contacto)
        def on_eliminar(e):
            print("DEBUG: on_eliminar -> eliminando id", id_contacto)
            ok, err = self.db.delete_contacto(id_contacto)
            if ok:
                # cerrar diálogo y refrescar
                self.page.dialog.open = False
                self.page.dialog = None
                self.cargar_contacto()
            else:
                print("Error al eliminar:", err)
                self.page.dialog.open = False

        dlg = ft.AlertDialog(
            title=ft.Text("Confirmar eliminación"),
            content=ft.Text("¿Seguro que deseas eliminar este contacto?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: (setattr(self.page, "dialog", None), self.page.update())),
                ft.ElevatedButton("Eliminar", on_click=on_eliminar)
            ]
        )
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()
