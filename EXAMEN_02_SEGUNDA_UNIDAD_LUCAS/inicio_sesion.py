# inicio_sesion.py
import flet as ft
from conexion import ConexionDB
from dashboard_view import DashboardView

class LoginView(ft.Container):
    def __init__(self, page: ft.Page, cambiar_vista):
        super().__init__(expand=True)
        self.page = page
        self.cambiar_vista = cambiar_vista
        self.conexion = ConexionDB()

        self.txt_usuario = ft.TextField(label="Usuario", width=250, value="admin")
        self.txt_password = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=250, value="1234")
        self.lbl_mensaje = ft.Text(value="", color="red")
        self.btn_ingresar = ft.ElevatedButton("Ingresar", on_click=self.login)

        self.content = ft.Column([ft.Text("🔐 Ingreso principal", size=22, weight="bold"), self.txt_usuario, self.txt_password, self.btn_ingresar, self.lbl_mensaje], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        self.alignment = ft.alignment.center

    def login(self, e):
        usuario = self.txt_usuario.value.strip()
        password = self.txt_password.value.strip()

        resultado = self.conexion.login_usuario(usuario, password)
        if resultado.get("status"):
            dashboard = DashboardView(self.page, self.cambiar_vista)
            self.cambiar_vista(dashboard)
        else:
            # si no tienes tabla usuarios, abre Dashboard directamente (descomenta)
            # dashboard = DashboardView(self.page, self.cambiar_vista)
            # self.cambiar_vista(dashboard)
            self.lbl_mensaje.value = "Usuario/contraseña incorrectos (o crea tabla usuarios)."
            self.lbl_mensaje.color = ft.Colors.RED
            self.update()
