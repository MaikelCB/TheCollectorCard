import flet as ft

class RegistroView:
    def __init__(self, page: ft.Page):
        self.page = page

    def mostrar(self):
        self.page.views.clear()

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
                    ft.TextField(
                        width=360,
                        height=40,
                        hint_text="Nombre/Usuario",
                        border="underline",
                        color="black",
                        prefix_icon=ft.icons.PERSON,
                    ),
                    padding=ft.padding.symmetric(horizontal=20, vertical=10)
                ),
                ft.Container(
                    ft.TextField(
                        width=360,
                        height=40,
                        hint_text="Correo electrónico",
                        border="underline",
                        color="black",
                        prefix_icon=ft.icons.EMAIL,
                    ),
                    padding=ft.padding.symmetric(horizontal=20, vertical=10)
                ),
                ft.Container(
                    ft.TextField(
                        width=360,
                        height=40,
                        hint_text="Contraseña",
                        border="underline",
                        color="black",
                        prefix_icon=ft.icons.LOCK,
                        password=True,
                    ),
                    padding=ft.padding.symmetric(horizontal=20, vertical=10)
                ),
                ft.Container(
                    ft.TextField(
                        width=360,
                        height=40,
                        hint_text="Confirmar contraseña",
                        border="underline",
                        color="black",
                        prefix_icon=ft.icons.LOCK,
                        password=True,
                    ),
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
        # Implementar lógica de registro de usuario
        pass
