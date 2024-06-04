import flet as ft

class LoginView:
    def __init__(self, page: ft.Page):
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.adaptive = True
        self.page = page

    def mostrar(self):
        self.page.views.clear()

        header = ft.Container(
            content=ft.Row(
                controls=[
                    ft.IconButton(icon=ft.icons.HOME, on_click=self.go_home),
                    ft.Row(
                        controls=[
                            ft.ElevatedButton("Registro", on_click=lambda _: self.page.go('/registro')),
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
                        "Iniciar Sesión",
                        width=320,
                        size=30,
                        text_align="center",
                        weight="w900",
                    ),
                    padding=ft.padding.only(20, 20)
                ),
                ft.Container(
                    ft.TextField(
                        width=280,
                        height=40,
                        hint_text="Correo electrónico",
                        border="underline",
                        color="black",
                        prefix_icon=ft.icons.EMAIL
                    ),
                    padding=ft.padding.only(20, 20)
                ),
                ft.Container(
                    ft.TextField(
                        width=280,
                        height=40,
                        hint_text="Contraseña",
                        border="underline",
                        color="black",
                        prefix_icon=ft.icons.LOCK,
                        password=True
                    ),
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
                        bgcolor="black"
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
                        ft.TextButton("Crear cuenta", on_click=lambda _: self.page.go('/registro'))
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
            "/login",
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

    def go_home(self, e):
        self.page.go('/')
