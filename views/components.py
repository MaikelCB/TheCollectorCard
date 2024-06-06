import flet as ft
from models.session import Session


def get_header(page: ft.Page):
    def go_home(e):
        page.go('/')

    def cerrar_sesion(e):
        print("Cerrando sesión...")  # Agregar declaración de impresión para depurar
        Session.logout()
        print("Sesión cerrada. Estado de la sesión:", Session.logged_in)
        # Redirigir a la vista de recarga
        page.go('/recargar?target=/')
        page.update()

    header_controls = [
        ft.IconButton(icon=ft.icons.HOME, on_click=go_home)
    ]

    if Session.logged_in:
        header_controls.append(ft.Row(
            controls=[
                ft.TextButton(Session.user_name),
                ft.TextButton("Cerrar sesión", on_click=cerrar_sesion)
            ],
            alignment=ft.MainAxisAlignment.END,
        ))
    else:
        header_controls.append(ft.Row(
            controls=[
                ft.ElevatedButton("Login", on_click=lambda _: page.go('/login/')),
                ft.ElevatedButton("Registro", on_click=lambda _: page.go('/registro/')),
            ],
            alignment=ft.MainAxisAlignment.END,
        ))

    return ft.Container(
        content=ft.Row(
            controls=header_controls,
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
