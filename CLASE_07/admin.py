import flet as ft

def main(page: ft.Page):
    def vista_administrador(page: ft.Page, nombre, logout_callback):
        page.clean()
        page.title = "Panel de Administrador"

    lista_usuarios = ft.Column()

    def actualizar_lista():
        lista_usuarios.controls.clear()
        for user, data in lista_usuarios.items():
            if user != "admi":
                fila = ft.Row([
                    ft.Text(f"{user} ({data['rol']})"),
                    ft.IconButton(
                        icon=ft.icons.DELETE,
                        tooltip="Eliminar",
                        on_click=lambda e, u=user: eliminar_usuario(u)
                    )
                ])
                lista_usuarios.controls.append(fila)
        page.update()

    def eliminar_usuario(usuario):
        dlg = ft.AlertDialog(
            title=ft.Text("Confirmar eliminación"),
            content=ft.Text(f"¿Seguro que deseas eliminar al usuario '{usuario}'?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: page.close(dlg)),
                ft.TextButton(
                    "Eliminar",
                    on_click=lambda e: (lista_usuarios.pop(usuario, None), actualizar_lista(), page.close(dlg))
                )
            ]
        )
        page.dialog = dlg
        dlg.open = True
        page.update()

    def agregar_usuario(e):
        nuevo = campo_usuario.value.strip()
        clave = campo_clave.value.strip()
        rol = dropdown_rol.value

        if not (nuevo and clave and rol):
            page.snack_bar = ft.SnackBar(ft.Text("⚠️ Completa todos los campos"), open=True)
            page.update()
            return

        if nuevo in lista_usuarios:
            page.snack_bar = ft.SnackBar(ft.Text("⚠️ El usuario ya existe"), open=True)
            page.update()
            return

        lista_usuarios[nuevo] = {"password": clave, "rol": rol}
        campo_usuario.value = ""
        campo_clave.value = ""
        dropdown_rol.value = None
        actualizar_lista()

    campo_usuario = ft.TextField(label="Nuevo usuario")
    campo_clave = ft.TextField(label="Contraseña", password=True)
    dropdown_rol = ft.Dropdown(label="Rol", options=[
        ft.dropdown.Option("usuario"),
        ft.dropdown.Option("admin")
    ])
    boton_agregar = ft.ElevatedButton("Agregar usuario", on_click=agregar_usuario)

    page.add(
        ft.Column([
            ft.Text(f"Bienvenido, {nombre} (Administrador)", size=24, weight=ft.FontWeight.BOLD), # type: ignore
            ft.Divider(),
            ft.Text("👥 Gestión de usuarios", size=18),
            campo_usuario,
            campo_clave,
            dropdown_rol,
            boton_agregar,
            ft.Divider(),
            lista_usuarios,
            ft.ElevatedButton("Cerrar sesión", icon=ft.icons.LOGOUT, on_click=lambda e: agregar_usuario())
        ], scroll=ft.ScrollMode.AUTO)
    )

    actualizar_lista()

ft.app(target=main)