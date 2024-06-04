import flet as ft
from control.digicard_control import DigiCardController

class HomeView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.digicard_controller = DigiCardController()
        self.card_row_container = ft.Container()
        self.details_panel = None
        self.current_page = 1
        self.cards_per_page = 54
        self.total_pages = 1
        self.all_cards = []
        self.pagination_container = ft.Container()  # Contenedor para botones de paginación
        self.digimon_visible = False

    def mostrar(self):
        self.page.views.clear()

        # Crear el encabezado (header)
        header = ft.Container(
            content=ft.Row(
                controls=[
                    ft.IconButton(icon=ft.icons.HOME, on_click=self.go_home),
                    ft.Row(
                        controls=[
                            ft.ElevatedButton("Login", on_click=lambda _: self.page.go('/login')),
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

        # Crear botones de categorías
        category_buttons = ft.Row(
            controls=[
                ft.ElevatedButton("Pokemon", on_click=self.cargar_pokemon),
                ft.ElevatedButton("Digimon", on_click=self.cargar_digimon),
                ft.ElevatedButton("Yugioh", on_click=self.cargar_yugioh),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )

        # Crear contenedor de cartas, inicialmente invisible
        self.card_row_container = ft.Container(
            margin=ft.margin.only(top=20),
            alignment=ft.alignment.center,
            expand=True,
            visible=False  # Inicialmente invisible
        )

        # Crear contenedor principal
        container = ft.Container(
            content=ft.Column(
                controls=[
                    header,
                    category_buttons,
                    self.card_row_container,
                    self.pagination_container  # Contenedor para botones de paginación
                ],
                alignment=ft.MainAxisAlignment.START,
                expand=True
            ),
            alignment=ft.alignment.center,
            padding=ft.padding.all(0),
            expand=True,
            margin=ft.margin.all(0)
        )

        # Añadir el contenedor a la vista
        self.page.views.append(ft.View(
            "/",
            controls=[container],
            padding=ft.padding.all(0),
            vertical_alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            bgcolor=ft.colors.BLACK
        ))

        self.page.update()

    def go_home(self, e):
        self.page.go('/')

    def toggle_cards(self, e):
        self.card_row_container.visible = not self.card_row_container.visible
        self.page.update()

    def cargar_pokemon(self, e):
        # Implementar lógica de carga de cartas de Pokemon
        pass

    def cargar_digimon(self, e):
        if self.digimon_visible:
            self.card_row_container.visible = False
            self.pagination_container.visible = False
            self.digimon_visible = False
        else:
            self.current_page = 1
            self.all_cards = self.digicard_controller.obtener_digicartas()
            self.all_cards.sort(key=lambda x: x.cardnumber)
            self.total_pages = (len(self.all_cards) + self.cards_per_page - 1) // self.cards_per_page
            self.mostrar_pagina(self.current_page)
            self.digimon_visible = True

    def cargar_yugioh(self, e):
        # Implementar lógica de carga de cartas de Yugioh
        pass

    def mostrar_pagina(self, pagina):
        start_index = (pagina - 1) * self.cards_per_page
        end_index = start_index + self.cards_per_page
        cards_to_show = self.all_cards[start_index:end_index]

        card_row = ft.Row(wrap=True, scroll=ft.ScrollMode.ALWAYS, expand=True)

        for carta in cards_to_show:
            image_proxy_url = f"{self.digicard_controller.proxy_url}{carta.image_url}"
            card_row.controls.append(
                ft.Container(
                    ft.Image(src=image_proxy_url, width=250, height=250),
                    border_radius=ft.border_radius.all(5),
                    padding=ft.padding.all(5),
                    on_click=lambda e, c=carta: self.mostrar_detalle_carta(c)
                )
            )

        self.card_row_container.content = card_row
        self.card_row_container.visible = True
        self.page.update()
        self.mostrar_paginacion()

    def mostrar_paginacion(self):
        if self.total_pages <= 1:
            self.pagination_container.visible = False
            self.page.update()
            return

        pagination_controls = []

        def add_button(page_number, text=None):
            text = text or str(page_number)
            button = ft.TextButton(text, on_click=lambda e, p=page_number: self.actualizar_pagina(p))
            if page_number == self.current_page:
                button.disabled = True  # Desactivar el botón de la página actual
            pagination_controls.append(button)

        add_button(1)
        if self.current_page > 3:
            pagination_controls.append(ft.Text("..."))

        start_page = max(2, self.current_page - 2)
        end_page = min(self.total_pages - 1, self.current_page + 2)

        for page in range(start_page, end_page + 1):
            add_button(page)

        if self.current_page < self.total_pages - 2:
            pagination_controls.append(ft.Text("..."))
        add_button(self.total_pages)

        pagination_row = ft.Row(
            controls=pagination_controls,
            alignment=ft.MainAxisAlignment.CENTER,
        )

        self.pagination_container.content = pagination_row
        self.pagination_container.visible = True
        self.page.update()

    def actualizar_pagina(self, pagina):
        self.current_page = pagina
        self.mostrar_pagina(pagina)

    def mostrar_detalle_carta(self, carta):
        # Cerrar cualquier panel de detalles abierto previamente
        if self.details_panel:
            self.page.overlay.remove(self.details_panel)

        image_proxy_url = f"{self.digicard_controller.proxy_url}{carta.image_url}"
        self.details_panel = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Image(src=image_proxy_url, width=300, height=300),
                    ft.Column(
                        controls=[
                            ft.Text(f"Name: {carta.name}", size=20, weight="bold"),
                            ft.Text(f"Type: {carta.type}"),
                            ft.Text(f"Color: {carta.color}"),
                            ft.Text(f"Stage: {carta.stage}"),
                            ft.Text(f"Rarity: {carta.cardrarity}"),
                            ft.Text(f"Set Name: {carta.set_name}"),
                            # Añadir más campos según sea necesario
                        ],
                        alignment=ft.MainAxisAlignment.START
                    )
                ],
                alignment=ft.MainAxisAlignment.START,
            ),
            alignment=ft.alignment.center,
            padding=ft.padding.all(0),
            bgcolor=ft.colors.WHITE,
            border_radius=ft.border_radius.all(10),
            shadow=ft.BoxShadow(
                color=ft.colors.BLACK,
                blur_radius=10,
                spread_radius=5,
                offset=ft.Offset(2, 2)
            )
        )

        # Añadir el panel de detalles como overlay
        self.page.overlay.append(self.details_panel)
        self.page.update()
