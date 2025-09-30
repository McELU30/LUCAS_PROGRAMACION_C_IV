import flet as ft
from admin import vista_administrador
from usuario import vista_usuario

# Simulación de base de datos
usuarios = {
    "admi": {"password": "75227199", "rol": "admin"},
    "juan": {"password": "927947371", "rol": "usuario"}
}

def main(page: ft.Page):
    page.title = "Login"
    page.window_width = 400
    page.window_height = 300

    # 🔄 Función que construye la pantalla de login
    def mostrar_login():
        page.clean()

        usuario = ft.TextField(label="Usuario")
        contraseña = ft.TextField(label="Contraseña", password=True, can_reveal_password=True)
        mensaje = ft.Text("", color="red")

        def login_click(e):
            mensaje.value = ""  
            user = usuario.value.strip()
            pwd = contraseña.value.strip()

            if user in usuarios and usuarios[user]["password"] == pwd:
                rol = usuarios[user]["rol"]
                if rol == "admin":
                    vista_administrador(page, user, mostrar_login)
                else:
                    vista_usuario(page, user, mostrar_login)
            else:
                mensaje.value = "⚠️ Credenciales incorrectas"
                page.update()

        contraseña.on_submit = login_click  

        page.add(
            ft.Column([
                ft.Text("🔐 Iniciar sesión", size=20, weight=ft.FontWeight.BOLD),
                usuario,
                contraseña,
                ft.ElevatedButton("Ingresar", on_click=login_click),
                mensaje
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )

    # Mostrar login por primera vez
    mostrar_login()

ft.app(target=main, view=ft.AppView.FLET_APP)
