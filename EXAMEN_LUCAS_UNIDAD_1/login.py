import flet as ft
import os
import sys
import threading
import time

# Usuario y contraseña válidos


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
        if usuario.value == "usuario" and contraseña.value == "123":
            abrir_dashboard()
        if usuario.value == "administrador" and contraseña.value == "123":
            abrir_administrador()
        if usuario.value == "visitante" and contraseña.value == "123":
            abrir_visitante()
        if usuario.value == "turista" and contraseña.value == "123":
            abrir_turista()
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
            import Dashboard
            Dashboard.main(page)

    def abrir_administrador():
        # En modo escritorio -> abrir dashboard.py como nuevo proceso
        if not page.web:
            page.window.close()
            ruta_dashboard = os.path.join(os.path.dirname(__file__), "administrador.py")
            subprocess.Popen([sys.executable, ruta_dashboard])
        else:
            # En modo web -> importar dashboard y cargarlo en la misma página
            import Dashboard
            Dashboard.main(page)

    def abrir_visitante():
        # En modo escritorio -> abrir dashboard.py como nuevo proceso
        if not page.web:
            page.window.close()
            ruta_dashboard = os.path.join(os.path.dirname(__file__), "visitante.py")
            subprocess.Popen([sys.executable, ruta_dashboard])
        else:
            # En modo web -> importar dashboard y cargarlo en la misma página
            import Dashboard
            Dashboard.main(page)

    def abrir_turista():
        # En modo escritorio -> abrir dashboard.py como nuevo proceso
        if not page.web:
            page.window.close()
            ruta_dashboard = os.path.join(os.path.dirname(__file__), "turista.py")
            subprocess.Popen([sys.executable, ruta_dashboard])
        else:
            # En modo web -> importar dashboard y cargarlo en la misma página
            import Dashboard
            Dashboard.main(page)
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
