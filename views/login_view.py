import flet as ft
import requests
from jose import jwt

from models.session import Session
from .components import get_header


class LoginView:
    def __init__(self, page: ft.Page):
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.adaptive = True
        self.page = page

    def mostrar(self):
        self.page.views.clear()

        self.username_or_email_input = ft.TextField(
            width=280,
            height=40,
            hint_text="Correo electrónico o Usuario",
            border="underline",
            color="black",
            prefix_icon=ft.icons.PERSON,
        )

        self.password_input = ft.TextField(
            width=280,
            height=40,
            hint_text="Contraseña",
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
                        "Iniciar Sesión",
                        width=320,
                        size=30,
                        text_align="center",
                        weight="w900",
                    ),
                    padding=ft.padding.only(20, 20)
                ),
                ft.Container(
                    self.username_or_email_input,
                    padding=ft.padding.only(20, 20)
                ),
                ft.Container(
                    self.password_input,
                    padding=ft.padding.only(20, 20)
                ),
                ft.Container(
                    ft.Checkbox(
                        label="Recordar contraseña",
                        check_color="black"
                    ),
                    padding=ft.padding.only(80)
                ),
                ft.Container(
                    ft.ElevatedButton(
                        text="INICIAR",
                        width=280,
                        bgcolor="black",
                        on_click=self.iniciar_sesion
                    ),
                    padding=ft.padding.only(20, 20)
                ),
                ft.Text("Iniciar sesión con",
                        text_align="center",
                        width=320,
                        ),
                ft.Container(
                    ft.Row([
                        ft.IconButton(
                            icon=ft.icons.EMAIL,
                            tooltip="Google",
                            icon_size=35
                        ),
                        ft.IconButton(
                            icon=ft.icons.FACEBOOK,
                            tooltip="Facebook",
                            icon_size=35
                        ),
                        ft.IconButton(
                            icon=ft.icons.APPLE,
                            tooltip="Apple",
                            icon_size=35
                        )
                    ],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    padding=ft.padding.only(20, 20)
                ),
                ft.Container(
                    ft.Row([
                        ft.Text("¿No tienes una cuenta?"),
                        ft.TextButton("Crear cuenta", on_click=lambda _: self.page.go('/registro/'))
                    ],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    padding=ft.padding.only(20, 20)

                )
            ],
                alignment=ft.MainAxisAlignment.SPACE_EVENLY
            ),
            alignment=ft.alignment.center,
            border_radius=20,
            width=320,
            height=500,
            gradient=ft.LinearGradient([
                ft.colors.PURPLE,
                ft.colors.PINK,
                ft.colors.RED,
            ]),
            padding=ft.padding.all(0),
            margin=ft.margin.all(0),
        )

        self.page.views.append(ft.View(
            "/login/",
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
            vertical_alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            bgcolor=ft.colors.BLACK,
            padding=ft.padding.all(0),
        ))

        self.page.update()

    def iniciar_sesion(self, e):
        username_or_email = self.username_or_email_input.value
        password = self.password_input.value

        try:
            response = requests.post(
                "http://127.0.0.1:8001/login/",
                data={
                    "username": username_or_email,
                    "password": password
                }
            )
            response.raise_for_status()

            result = response.json()
            if response.status_code == 200:
                print("Login successful:", result)
                token = result["access_token"]

                # Obtener el ID de usuario y nombre de usuario
                user_response = requests.get(
                    "http://127.0.0.1:8001/me/",
                    headers={"Authorization": f"Bearer {token}"}
                )
                user_response.raise_for_status()
                user_info = user_response.json()

                # Establecer el estado de la sesión
                Session.login(user_info["id"], user_info["nombre"])
                self.page.go('/user/')
            else:
                if "detail" in result:
                    print("Login failed:", result["detail"])

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

    def go_home(self, e):
        self.page.go('/')
