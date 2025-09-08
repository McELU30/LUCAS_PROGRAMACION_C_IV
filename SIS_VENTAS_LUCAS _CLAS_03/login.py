import flet as ft
import os
import sys

def main(page: ft.Page):
    # SOLO configurar ventana si NO es web
    if not page.web:
        page.window.width = 500
        page.window.height = 200
        page.window.resizable = False
        page.window.center()

    page.title = "Segunda clase - Programación Concurrente"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.update()
    
    def abrir_ventana_carga(tipo):
        if page.web:
            # En MODO WEB: mostrar la carga en la misma página
            mostrar_carga_en_pagina(tipo)
        else:
            # En MODO DESKTOP: cerrar y abrir nueva ventana
            page.window.close()
            ruta_script = os.path.join(os.path.dirname(__file__), "S_carga.py")
            import subprocess
            subprocess.Popen([sys.executable, ruta_script, tipo])
    
    def mostrar_carga_en_pagina(tipo):
        page.clean()
        
        # Simular la interfaz de S_carga.py en la misma página
        progress_ring = ft.ProgressRing(width=100, height=100, stroke_width=10)
        texto_carga = ft.Text(f"¡{tipo.upper()} en proceso!", size=20, weight=ft.FontWeight.BOLD)
        texto_estado = ft.Text("Por favor espere...", size=14)
        
        page.add(
            ft.Column([
                progress_ring,
                ft.Divider(height=20),
                texto_carga,
                ft.Divider(height=10),
                texto_estado
            ], 
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )
        page.update()
        
        # Simular carga
        import threading
        import time
        
        def simular_carga_web():
            for i in range(1, 101):
                time.sleep(0.05)
                texto_estado.value = f"Progreso: {i}%"
                page.update()
            
            time.sleep(0.2)
            texto_estado.value = "¡Operación completada!"
            progress_ring.value = 1.0
            page.update()
            
            time.sleep(1)
            # Redirigir según el tipo
            if tipo == "login":
                mostrar_dashboard()
            else:
                mostrar_portada()
        
        threading.Thread(target=simular_carga_web, daemon=True).start()
    
    def mostrar_dashboard():
        page.clean()
        page.add(
            ft.Column([
                ft.Text("🎯 DASHBOARD PRINCIPAL", size=30, weight=ft.FontWeight.BOLD, color="#2196F3"),
                ft.Text("Bienvenido al Dashboard", size=18),
                ft.ElevatedButton("Volver al menú", on_click=lambda e: volver_menu())
            ], alignment=ft.MainAxisAlignment.CENTER)
        )
        page.update()
    
    def mostrar_portada():
        page.clean()
        page.add(
            ft.Column([
                ft.Text("🛍️ PORTADA DE COMPRAS", size=30, weight=ft.FontWeight.BOLD, color="#4CAF50"),
                ft.Text("Bienvenido a la Portada", size=18),
                ft.ElevatedButton("Volver al menú", on_click=lambda e: volver_menu())
            ], alignment=ft.MainAxisAlignment.CENTER)
        )
        page.update()
    
    def volver_menu():
        page.clean()
        page.add(contenido_principal)
        page.update()
    
    def compra_click(e):
        abrir_ventana_carga("compra")

    def login_click(e):
        abrir_ventana_carga("login")

    btn_compra = ft.ElevatedButton(
        text="🛒 Realizar compra",
        width=200,  
        height=100,
        bgcolor="#4CAF50",
        color="white",
        on_click=compra_click
    )

    btn_login = ft.ElevatedButton(
        text="🔑 Iniciar sesión",
        width=200,  
        height=100,
        bgcolor="#2196F3",
        color="white",
        on_click=login_click
    )

    # Guardar el contenido principal para poder volver
    contenido_principal = ft.Row(
        [btn_compra, btn_login],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20
    )

    page.add(contenido_principal)
    page.update()

if __name__ == "__main__":
    ft.app(target=main)