# main.py
import flet as ft
from inicio_sesion import LoginView

def main(page: ft.Page):
    page.title = "celular"
    page.window_width = 1000
    page.window_height = 700

    def cambiar_vista(vista):
        page.clean()
        page.add(vista)
        page.update()

    login = LoginView(page, cambiar_vista)
    cambiar_vista(login)

ft.app(target=main)
