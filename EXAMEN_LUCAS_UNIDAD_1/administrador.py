
import flet as ft
import os
import sys
import subprocess
import asyncio

def main(page: ft.Page):
    page.window.width = 800
    page.window.height = 600
    page.window.resizable = True
    page.window.center()
    page.title = "Sistema - Online de Reservaciones o venta de Cupos para Viajes Turísticos En el Modo Usuario"

    # Variables dinámicas
    mensaje = ft.Text("", size=16, color="BLUE", weight=ft.FontWeight.BOLD)
    contador = ft.Text("Cupos reservados: 0", size=18, color="red", weight=ft.FontWeight.BOLD)
    cupos_reservados = {"cantidad": 0}  # usamos dict para que sea mutable dentro de funciones

    def volver_inicio(e):
        page.window.close()
        ruta_main = os.path.join(os.path.dirname(__file__), "main.py")
        subprocess.Popen([sys.executable, ruta_main])

    # Función asíncrona para simular reserva
    async def reservar_cupo_async():
        mensaje.value = "⏳ Reservando cupo..."
        page.update()
        await asyncio.sleep(2)  # simula tiempo de proceso
        cupos_reservados["cantidad"] += 1  # aumenta contador
        mensaje.value = "✅ Cupo reservado con éxito"
        contador.value = f"Cupos reservados: {cupos_reservados['cantidad']}"
        page.update()

    def reservar_cupo(e):
        page.run_task(reservar_cupo_async)

    # Layout del dashboard
    page.add(
        ft.Column(
            [
                ft.Text("🌈 RESERVACIONES DE CUPOS Y VENTAS EN EL MODO USUARIO PARA VIAJES TURÍSTICOS POR EL PERÚ ☄",
                        size=29, weight=ft.FontWeight.BOLD, color="#14EE10"),
                ft.Divider(height=20),
                ft.Text("Bienvenido al sistema de gestión de ventas en modo usuario online Turístico", size=18),
                ft.Divider(height=30),
                ft.Row(
                    [
                        ft.ElevatedButton("Ver Reportes de Reserva"),
                        ft.ElevatedButton("Reservar Cupo", on_click=reservar_cupo),
                        ft.ElevatedButton("Modo Usuario"),
                    ],
                    spacing=20
                ),
                mensaje,
                contador,  # mostramos el contador debajo
                ft.Divider(height=30),
                ft.ElevatedButton("Volver al Inicio y cerrar sesión", on_click=volver_inicio)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

if __name__ == "__main__":
    ft.app(target=main)