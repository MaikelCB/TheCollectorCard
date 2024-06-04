import flet as ft

class RegistroView:
    def __init__(self, page: ft.Page):
        self.page = page

    def mostrar(self):
        self.page.views.clear()

        container = ft.Container(
            ft.Column([
                ft.Container(
                    ft.Text(
                        "Registro",
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
                        text="REGISTRARSE",
                        width=280,
                        bgcolor="black"
                    ),
                    padding=ft.padding.only(20, 20)
                ),
                ft.Text("Registrarse con",
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
                        ft.Text("¿Ya tienes una cuenta?"),
                        ft.TextButton("Iniciar sesión", on_click=lambda _: self.page.go('/login'))
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
            "/registro",
            controls=[container],
            padding=ft.padding.all(0),
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            bgcolor=ft.colors.BLACK
        ))
        self.page.update()
        