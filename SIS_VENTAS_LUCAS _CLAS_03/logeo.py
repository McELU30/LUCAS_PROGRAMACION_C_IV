import flet as ft
import os
import sys
import threading
import time

# Usuario y contraseña válidos
USUARIO_VALIDO = "admin"
CONTRASEÑA_VALIDA = "1234"

def main(page: ft.Page):
    # Configuración ventana (solo desktop)
    if not page.web:
        page.window.width = 500
        page.window.height = 300
        page.window.resizable = False
        page.window.center()

    page.title = "Login - Sistema de Ventas"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # ========================= LOGIN =========================
    usuario = ft.TextField(label="Usuario", width=300)
    contraseña = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=300)
    mensaje_login = ft.Text("", color="red")

    def validar_login(e):
        if usuario.value == USUARIO_VALIDO and contraseña.value == CONTRASEÑA_VALIDA:
            abrir_dashboard()
        else:
            mensaje_login.value = "❌ Usuario o contraseña incorrectos"
            page.update()

    def abrir_dashboard():
        # En modo escritorio -> abrir dashboard.py como nuevo proceso
        if not page.web:
            page.window.close()
            ruta_dashboard = os.path.join(os.path.dirname(__file__), "dashboard.py")
            subprocess.Popen([sys.executable, ruta_dashboard])
        else:
            # En modo web -> importar dashboard y cargarlo en la misma página
            import dashboard
            dashboard.main(page)

    import subprocess

    login_form = ft.Column([
        ft.Text("🔑 Iniciar Sesión", size=25, weight=ft.FontWeight.BOLD, color="#2196F3"),
        usuario,
        contraseña,
        mensaje_login,
        ft.ElevatedButton("Entrar", on_click=validar_login),
    ], alignment=ft.MainAxisAlignment.CENTER,
       horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    page.add(login_form)
    page.update()

if __name__ == "__main__":
    ft.app(target=main)
