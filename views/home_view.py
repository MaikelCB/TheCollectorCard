import flet as ft
from control.digicard_control import DigiCardController
from models.digicoleccion import DigiColeccion

class HomeView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.digicard_controller = DigiCardController()
        self.card_row_container = ft.Container()

    def mostrar(self):
        self.page.views.clear()

        # Crear botones de navegación
        buttons = ft.Row(
            controls=[
                ft.ElevatedButton("Login", on_click=lambda _: self.page.go('/login')),
                ft.ElevatedButton("Registro", on_click=lambda _: self.page.go('/registro')),
                ft.ElevatedButton("BT-01: Booster New Evolution", on_click=self.toggle_cards),
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )

        # Llamar al controlador para obtener las cartas del set "BT-01: Booster New Evolution"
        set_name_filter = "BT-01: Booster New Evolution"
        cartas = self.digicard_controller.obtener_digicartas(set_name_filter)
        colecciones = {}

        # Crear fila de cartas
        card_row = ft.Row(wrap=True, scroll=ft.ScrollMode.ALWAYS, expand=True)

        for carta in cartas:
            if carta.set_name not in colecciones:
                colecciones[carta.set_name] = DigiColeccion(carta.set_name)
            colecciones[carta.set_name].agregar_carta(carta)
            image_proxy_url = f"{self.digicard_controller.proxy_url}{carta.image_url}"
            card_row.controls.append(
                ft.Container(
                    ft.Image(src=image_proxy_url, width=250, height=250),
                    border_radius=ft.border_radius.all(5),
                    padding=ft.padding.all(5)
                )
            )

        # Crear contenedor de cartas, inicialmente invisible
        self.card_row_container = ft.Container(
            content=card_row,
            margin=ft.margin.only(top=20),
            alignment=ft.alignment.center,
            expand=True,
            visible=False  # Inicialmente invisible
        )

        # Crear contenedor principal
        container = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Bienvenido a la página principal", size=24, weight="bold"),
                    buttons,
                    self.card_row_container
                ],
                alignment=ft.MainAxisAlignment.START,
            ),
            alignment=ft.alignment.center,
            padding=ft.padding.all(20),
            expand=True
        )

        # Añadir el contenedor a la vista
        self.page.views.append(ft.View(
            "/",
            controls=[container],
        ))

        self.page.update()

    def toggle_cards(self, e):
        self.card_row_container.visible = not self.card_row_container.visible
        self.page.update()
