# dashboard_view.py
import flet as ft
from contacto.contacto_view import ContactoView

class DashboardView(ft.Container):
    def __init__(self, page, cambiar_vista):
        super().__init__(expand=True)
        self.page = page
        self.cambiar_vista = cambiar_vista

        titulo = ft.Text("📘 Panel Principal – tu contacto", size=24, weight="bold")

        tablas = [("contacto", "Datos básicos (Datos contacto)"),]

        grid = ft.GridView(expand=True, runs_count=3, max_extent=280, child_aspect_ratio=1.2, spacing=10, run_spacing=10)

        for nombre, descripcion in tablas:
            card_content = ft.Container(
                content=ft.Column([ft.Text(nombre, size=18, weight="bold"), ft.Text(descripcion, size=13, color=ft.Colors.GREY)], spacing=5),
                padding=15, border_radius=10, bgcolor=ft.Colors.BLUE_50, ink=True,
                on_click=lambda e, n=nombre: self.mostrar_tabla(n)
            )
            grid.controls.append(ft.Card(content=card_content, elevation=3))

        self.content = ft.Column([titulo, grid], expand=True, scroll=ft.ScrollMode.AUTO, horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.START)

    def mostrar_tabla(self, nombre_tabla):
        print("DEBUG: mostrar_tabla:", nombre_tabla)
        if nombre_tabla == "contacto":
            self.abrir_contacto()
        else:
            dlg = ft.AlertDialog(title=ft.Text("Tabla no implementada"), content=ft.Text(f"La vista para '{nombre_tabla}' aún no está disponible."), actions=[ft.TextButton("Cerrar", on_click=lambda e: self.page.dialog.close())])
            self.page.dialog = dlg
            dlg.open = True
            self.page.update()

    def abrir_contacto(self):
        def volver_o_navegar(nueva_vista=None):
            if nueva_vista is None:
                self.cambiar_vista(DashboardView(self.page, self.cambiar_vista))
            else:
                self.cambiar_vista(nueva_vista)
        self.cambiar_vista(ContactoView(self.page, volver_atras=volver_o_navegar))
