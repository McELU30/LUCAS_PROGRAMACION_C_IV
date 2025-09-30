import flet as ft
import os
import sys

def main(page: ft.Page):
    # Configuración ventana (solo desktop)
    if not page.web:
        page.window.width = 800
        page.window.height = 600
        page.window.resizable = True
        page.window.center()

    page.title = "Dashboard - Sistema de viajes para vicitante"

    def mostrar_dashboard():
        page.clean()
        page.add(
            ft.Column([
                ft.Text(" 🚗 BIEN VENIDO ALA VENTA DE VIAJES ", size=30, weight=ft.FontWeight.BOLD, color="#2196F3"),
                ft.Divider(height=20),
                ft.Text("Aga sus reservas", size=18),
                ft.Divider(height=30),
                ft.Row([
                    ft.ElevatedButton("📊 fotos"),
                    ft.ElevatedButton("📦 hacer reserva"),
                    ft.ElevatedButton("👥 ver precios"),
                ], spacing=20),
                ft.Divider(height=30),
                ft.ElevatedButton("Cerrar Sesión", on_click=lambda e: volver_inicio())
            ], alignment=ft.MainAxisAlignment.CENTER,
               horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )
        page.update()

    def volver_inicio():
        if not page.web:
            page.window.close()
            ruta_main = os.path.join(os.path.dirname(__file__), "login.py")
            import subprocess
            subprocess.Popen([sys.executable, ruta_main])
        else:
            # En modo web, simulamos volver al login
            main.main(page)
 
    # Mostrar dashboard al iniciar
    mostrar_dashboard()

if __name__ == "__main__":
    ft.app(target=main)
