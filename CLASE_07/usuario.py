import flet as ft

def vista_usuario(page: ft.Page, nombre, logout_callback):
    page.clean()
    page.title = "Vista Usuario"

    page.add(
        ft.Column([
            ft.Text(f"Bienvenido, {nombre} (Usuario)", size=24, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            ft.Text("👤 Esta es tu vista personal.", size=18),
            ft.Divider(),
            ft.ElevatedButton(
                "Cerrar sesión",
                icon=ft.icons.LOGOUT,
                on_click=lambda e: logout_callback()
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20)
    )
