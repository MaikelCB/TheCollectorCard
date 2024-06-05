import flet as ft
from control.user_control import UsuarioController


class RegistroView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.controller = UsuarioController()

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

        header = ft.Container(
            content=ft.Row(
                controls=[
                    ft.IconButton(icon=ft.icons.HOME, on_click=lambda _: self.page.go('/')),
                    ft.Row(
                        controls=[
                            ft.ElevatedButton("Login", on_click=lambda _: self.page.go('/login')),
                        ],
                        alignment=ft.MainAxisAlignment.END,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[ft.colors.GREEN, ft.colors.BLUE],
            ),
            padding=ft.padding.all(10),
            margin=ft.margin.all(0),
            expand=False,
        )

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
                        ft.TextButton("Iniciar sesión", on_click=lambda _: self.page.go('/login'))
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
            "/registro",
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

        result = self.controller.registrar_usuario(nombre, email, password)

        if result["status"] == "error":
            if "ErrorEmail" in result["message"]:
                self.email_input.bgcolor = ft.colors.BLACK
            if "ErrorPWD" in result["message"]:
                self.password_input.bgcolor = ft.colors.BLACK
                self.confirm_password_input.bgcolor = ft.colors.BLACK
            self.page.update()
        else:
            self.page.go("/login")
