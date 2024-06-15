import flet as ft
from models.session import Session
from control.digicard_control import DigiCardController

digicard_controller = DigiCardController()


def get_header(page: ft.Page):
    def go_home(e):
        page.go('/')

    def cerrar_sesion(e):
        print("Cerrando sesión...")
        Session.logout()
        print("Sesión cerrada. Estado de la sesión:", Session.logged_in)
        page.go('/')
        page.update()

    header_controls = [
        ft.Container(
            ft.Image(
                src='Logo.png',
            height=50),
            border_radius=ft.border_radius.all(5),
            padding=ft.padding.all(0),
            on_click=go_home
        )
    ]

    if Session.logged_in:
        header_controls.append(ft.Row(
            controls=[
                ft.TextButton(Session.user_name, on_click=lambda _: page.go('/user/')),
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
            colors=[ft.colors.PURPLE, ft.colors.BLUE],
        ),
        padding=ft.padding.all(10),
        margin=ft.margin.all(0),
        expand=False,
        alignment=ft.alignment.top_center,
    )


def crear_texto(contenido, size=16, weight=None):
    return ft.Text(contenido, size=size, weight=weight, color=ft.colors.BLACK)


def mostrar_detalle_carta(page, carta, cerrar_panel_detalles):
    # Construir la URL de la imagen proxy
    image_proxy_url = carta.image_url

    # Crear la lista de controles con todos los detalles de la carta
    detalles_carta = [
        crear_texto(f"Name: {carta.name}", size=22, weight="bold"),
        crear_texto(f"Card Number: {carta.id}", size=20, weight="bold"),
        crear_texto(f"Type: {carta.type}"),
        crear_texto(f"Color: {carta.color}"),
        crear_texto(f"Stage: {carta.stage}"),
        crear_texto(f"Digi Type: {carta.digi_type}"),
        crear_texto(f"Attribute: {carta.attribute}"),
        crear_texto(f"Level: {carta.level}"),
        crear_texto(f"Play Cost: {carta.play_cost}"),
        crear_texto(f"Evolution Cost: {carta.evolution_cost}"),
        crear_texto(f"Rarity: {carta.rarity}"),
        crear_texto(f"Artist: {carta.artist}"),
        crear_texto(f"DP: {carta.dp}"),
    ]

    # Crear los textos de Main Effect y Source Effect
    main_effect_text = crear_texto(f"Main Effect: {carta.main_effect}")
    source_effect_text = crear_texto(f"Source Effect: {carta.source_effect}")

    # Crear el contenedor de detalles de la carta
    details_panel = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Image(src=image_proxy_url, width=400, height=450),
                        ft.Column(
                            controls=detalles_carta,
                            alignment=ft.MainAxisAlignment.START,
                            scroll=ft.ScrollMode.AUTO,  # Añadir scroll si los detalles son demasiados
                            width=300  # Ajustar el ancho de la columna de detalles
                        )
                    ],
                    alignment=ft.MainAxisAlignment.START,
                ),
                ft.Container(
                    content=main_effect_text,
                    padding=ft.padding.only(33)  # Añadir margen horizontal
                ),
                ft.Container(
                    content=source_effect_text,
                    padding=ft.padding.only(33)  # Añadir margen horizontal
                )
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=10
        ),
        alignment=ft.alignment.center,
        padding=ft.padding.all(10),
        bgcolor=ft.colors.CYAN,
        border_radius=ft.border_radius.all(10),
        shadow=ft.BoxShadow(
            color=ft.colors.BLACK,
            blur_radius=10,
            spread_radius=5,
            offset=ft.Offset(2, 2)
        ),
        width=720,  # Ancho del panel
        height=620,  # Alto del panel
        on_click=cerrar_panel_detalles  # Manejar click fuera del panel
    )

    # Añadir el panel de detalles como overlay
    page.overlay.append(details_panel)
    page.update()
    return details_panel


def get_footer(page: ft.Page):
    footer_controls = [
        ft.Text("© 2024 The Collector Card App. All rights reserved."),
        ft.Row(
            controls=[
                ft.TextButton("Privacy Policy", on_click=lambda _: print("Privacy Policy clicked")),
                ft.TextButton("Terms of Service", on_click=lambda _: print("Terms of Service clicked")),
                ft.TextButton("Contact Us", on_click=lambda _: print("Contact Us clicked"))
            ],
            alignment=ft.MainAxisAlignment.END,
        )
    ]

    return ft.Container(
        content=ft.Row(
            controls=footer_controls,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        gradient=ft.LinearGradient(
            begin=ft.alignment.bottom_right,
            end=ft.alignment.top_left,
            colors=[ft.colors.PURPLE, ft.colors.BLUE],
        ),
        padding=ft.padding.all(10),
        margin=ft.margin.all(0),
        expand=False,
        alignment=ft.alignment.bottom_center,
    )
