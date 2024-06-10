import flet as ft
from control.digicard_control import DigiCardController
from .components import get_header, mostrar_detalle_carta
from models.session import Session


class UserView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.digicard_controller = DigiCardController()
        self.card_row_container = ft.Container()
        self.details_panel = None
        self.current_page = 1
        self.cards_per_page = 54
        self.total_pages = 1
        self.all_cards = []
        self.filtrado_container = ft.Container()  # Contenedor para filtrado
        self.pagination_container = ft.Container()  # Contenedor para paginación
        self.digimon_visible = False

    def mostrar(self):
        self.page.views.clear()

        # Crear el encabezado (header)
        header = get_header(self.page)

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
                    self.filtrado_container,
                    self.card_row_container,
                    self.pagination_container
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
            "/user/",
            controls=[container],
            padding=ft.padding.all(0),
            vertical_alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            bgcolor=ft.colors.BLACK
        ))

        self.page.update()

    def go_home(self, e):
        self.page.go('/')

    def cargar_pokemon(self, e):
        # Implementar lógica de carga de cartas de Pokemon
        pass

    def cargar_digimon(self, e):
        if self.digimon_visible:
            self.filtrado_container.visible = False
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
        self.page.update()

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
            cantidad = self.digicard_controller.obtener_cantidad_carta(Session.user_id, carta.cardnumber)
            card_row.controls.append(self.crear_carta(carta, image_proxy_url, cantidad))

        self.mostrar_filtro()
        self.card_row_container.content = card_row
        self.card_row_container.visible = True
        self.page.update()
        self.mostrar_paginacion()

    def crear_carta(self, carta, image_proxy_url, cantidad_inicial):
        cantidad = ft.Text(str(cantidad_inicial), size=20, color="white")

        def incrementar(e):
            nueva_cantidad = int(cantidad.value) + 1
            cantidad.value = str(nueva_cantidad)
            self.digicard_controller.actualizar_cantidad_carta(Session.user_id, carta.cardnumber, nueva_cantidad)
            self.page.update()

        def decrementar(e):
            nueva_cantidad = int(cantidad.value) - 1
            if nueva_cantidad >= 0:
                cantidad.value = str(nueva_cantidad)
                self.digicard_controller.actualizar_cantidad_carta(Session.user_id, carta.cardnumber, nueva_cantidad)
                self.page.update()

        return ft.Container(
            content=ft.Column(
                [
                    ft.Container(
                        content=ft.Image(
                            src=image_proxy_url,
                            width=250,
                            height=310,
                            fit=ft.ImageFit.COVER,
                            border_radius=ft.border_radius.all(0)
                        ),
                        on_click=lambda e, c=carta: self.mostrar_detalle_carta(c),
                    ),
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.IconButton(icon=ft.icons.REMOVE, on_click=decrementar),
                                cantidad,
                                ft.IconButton(icon=ft.icons.ADD, on_click=incrementar),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_AROUND,
                        ),
                        bgcolor=ft.colors.BLUE,
                        padding=ft.padding.all(0),
                        border_radius=ft.border_radius.all(0),
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=0,
            ),
            border_radius=ft.border_radius.all(10),
            padding=ft.padding.all(0),
            width=250,
            height=350,
        )

    def mostrar_filtro(self):
        filtrado_row = ft.Row(
            controls=[
                ft.Text("Filtro"),
                ft.IconButton(icon=ft.icons.FILTER_LIST)
            ],
            alignment=ft.MainAxisAlignment.END,
        )
        self.filtrado_container.content = filtrado_row
        self.filtrado_container.visible = True
        self.page.update()

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

        # Construir la URL de la imagen proxy
        self.details_panel = mostrar_detalle_carta(self.page, carta, self.cerrar_panel_detalles)

    def cerrar_panel_detalles(self, e):
        # Cerrar el panel de detalles si se hace clic fuera de él
        self.page.overlay.remove(self.details_panel)
        self.details_panel = None
        self.page.update()
