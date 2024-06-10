import flet as ft
import requests
from .components import get_header

class RegistroView:
    def __init__(self, page: ft.Page):
        self.page = page

    def mostrar(self):
        self.page.views.clear()

        self.nombre_input = ft.TextField(
            width=360,
            height=40,
            hint_text="Nombre/Usuario",
            border="underline",
            color="black",
            prefix_icon=ft.icons.PERSON,
        )

        self.email_input = ft.TextField(
            width=360,
            height=40,
            hint_text="Correo electrónico",
            border="underline",
            color="black",
            prefix_icon=ft.icons.EMAIL,
        )

        self.password_input = ft.TextField(
            width=360,
            height=40,
            hint_text="Contraseña",
            border="underline",
            color="black",
            prefix_icon=ft.icons.LOCK,
            password=True,
        )

        self.confirm_password_input = ft.TextField(
            width=360,
            height=40,
            hint_text="Confirmar contraseña",
            border="underline",
            color="black",
            prefix_icon=ft.icons.LOCK,
            password=True,
        )

        header = get_header(self.page)

        container = ft.Container(
            ft.Column([
                ft.Container(
                    ft.Text(
                        "Registro",
                        width=400,
                        size=30,
                        text_align="center",
                        weight="w900",
                    ),
                    padding=ft.padding.only(top=20, bottom=20)
                ),
                ft.Container(
                    self.nombre_input,
                    padding=ft.padding.symmetric(horizontal=20, vertical=10)
                ),
                ft.Container(
                    self.email_input,
                    padding=ft.padding.symmetric(horizontal=20, vertical=10)
                ),
                ft.Container(
                    self.password_input,
                    padding=ft.padding.symmetric(horizontal=20, vertical=10)
                ),
                ft.Container(
                    self.confirm_password_input,
                    padding=ft.padding.symmetric(horizontal=20, vertical=10)
                ),
                ft.Container(
                    ft.ElevatedButton(
                        text="REGISTRARSE",
                        width=360,
                        bgcolor="black",
                        on_click=self.registrar_usuario
                    ),
                    padding=ft.padding.symmetric(horizontal=20, vertical=10)
                ),
                ft.Container(
                    ft.Row([
                        ft.Text("¿Ya tienes una cuenta?"),
                        ft.TextButton("Iniciar sesión", on_click=lambda _: self.page.go('/login/'))
                    ],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    padding=ft.padding.symmetric(horizontal=20, vertical=10)
                )
            ],
                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            alignment=ft.alignment.center,
            border_radius=20,
            width=550,
            height=900,
            gradient=ft.LinearGradient([
                ft.colors.PURPLE,
                ft.colors.PINK,
                ft.colors.RED,
            ]),
            padding=ft.padding.all(0),
            margin=ft.margin.all(0),
        )

        self.page.views.append(ft.View(
            "/registro/",
            controls=[
                ft.Column(
                    [
                        header,
                        ft.Container(
                            container,
                            alignment=ft.alignment.center,
                            expand=True,
                            margin=ft.margin.symmetric(vertical=20)
                        ),
                    ],
                    expand=True,
                )
            ],
            padding=ft.padding.all(0),
            vertical_alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            bgcolor=ft.colors.BLACK
        ))
        self.page.update()

    def registrar_usuario(self, e):
        nombre = self.nombre_input.value
        email = self.email_input.value
        password = self.password_input.value
        confirm_password = self.confirm_password_input.value

        if password != confirm_password:
            self.password_input.value = ""
            self.confirm_password_input.value = ""
            self.page.update()
            return

        # Hacer una solicitud POST a la API para registrar el usuario
        try:
            response = requests.post(
                "http://127.0.0.1:8001/usuarios/",
                json={
                    "nombre": nombre,
                    "email": email,
                    "password": password,
                    "confirm_password": confirm_password
                }
            )
            response.raise_for_status()

            # Verificar si la respuesta es JSON
            if response.headers.get("content-type") == "application/json":
                result = response.json()
            else:
                result = {}

            if response.status_code == 200:
                self.page.go("/login/")
            else:
                if "detail" in result:
                    if "Invalid email" in result["detail"]:
                        self.email_input.bgcolor = ft.colors.RED
                    if "Password too short" in result["detail"]:
                        self.password_input.bgcolor = ft.colors.RED
                        self.confirm_password_input.bgcolor = ft.colors.RED
                    if "Passwords do not match" in result["detail"]:
                        self.password_input.value = ""
                        self.confirm_password_input.value = ""
                self.page.update()
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
