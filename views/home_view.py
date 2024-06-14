import flet as ft
from control.digicard_control import DigiCardController
from .components import get_header, get_footer, mostrar_detalle_carta


class HomeView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.digicard_controller = DigiCardController()
        self.details_panel = None
        self.current_page = 1
        self.cards_per_page = 54
        self.total_pages = 1
        self.all_cards = []
        self.category_container = ft.Container()
        self.card_row_container = ft.Container()
        self.filtrado_container = ft.Container()  # Contenedor para filtrado
        self.pagination_container = ft.Container()  # Contenedor para paginación
        self.digimon_visible = False

    def mostrar(self):
        self.page.views.clear()
        self.filtrado_container.visible = False
        self.card_row_container.visible = False
        self.pagination_container.visible = False

        header = get_header(self.page)
        footer = get_footer(self.page)

        category_containers1 = [
            ft.Container(
                ft.Image(
                    src=self.digicard_controller.obtener_bannermagic_image(),
                    width=550,
                    height=170),
                border_radius=ft.border_radius.all(5),
                padding=ft.padding.all(5),
                on_click=self.cargar_magic
            ),
            ft.Container(
                ft.Image(
                    src=self.digicard_controller.obtener_bannerdigimon_image(),
                    width=550,
                    height=170),
                border_radius=ft.border_radius.all(5),
                padding=ft.padding.all(5),
                on_click=self.cargar_digimon
            ),
            ft.Container(
                ft.Image(
                    src=self.digicard_controller.obtener_banneryugioh_image(),
                    width=550,
                    height=170),
                border_radius=ft.border_radius.all(5),
                padding=ft.padding.all(5),
                on_click=self.cargar_yugioh
            )]
        category_containers2 = [

            ft.Container(
                ft.Image(
                    src=self.digicard_controller.obtener_bannerpokemon_image(),
                    width=550,
                    height=170),
                border_radius=ft.border_radius.all(5),
                padding=ft.padding.all(5),
                on_click=self.cargar_pokemon
            ),
            ft.Container(
                ft.Image(
                    src=self.digicard_controller.obtener_banneronepiece_image(),
                    width=550,
                    height=170),
                border_radius=ft.border_radius.all(5),
                padding=ft.padding.all(5),
                on_click=self.cargar_onepiece
            ),
            ft.Container(
                ft.Image(
                    src=self.digicard_controller.obtener_bannerlorcana_image(),
                    width=550,
                    height=170),
                border_radius=ft.border_radius.all(5),
                padding=ft.padding.all(5),
                on_click=self.cargar_lorcana
            ),
        ]

        category1_row = ft.Row(
            controls=category_containers1,
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
        )
        category2_row = ft.Row(
            controls=category_containers2,
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
        )

        self.category_container = ft.Container(
            content=ft.Column(
                controls=[category1_row, category2_row]
            ),
        )

        # Crear contenedor de cartas, inicialmente invisible
        self.card_row_container = ft.Container(

            margin=ft.margin.only(top=20),
            alignment=ft.alignment.center,
            expand=False,
            offset=ft.transform.Offset(-2, 0),
            animate_offset=ft.animation.Animation(1000),
        )

        # Crear contenedor principal
        container = ft.Container(

            content=ft.Column(
                controls=[
                    header,
                    self.category_container,
                    self.filtrado_container,
                    self.card_row_container,
                    self.pagination_container,
                    footer
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                expand=True,
                scroll=ft.ScrollMode.ALWAYS

            ),
            alignment=ft.alignment.top_center,
            padding=ft.padding.all(0),
            expand=True,
            margin=ft.margin.all(0),
        )

        # Añadir el contenedor a la vista
        self.page.views.append(ft.View(
            "/",
            controls=[container],
            padding=ft.padding.all(0),
            vertical_alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            bgcolor=ft.colors.BLACK,
        ))

        self.page.update()

    def go_home(self, e):
        self.page.go('/')

    def cargar_digimon(self, e):
        if self.digimon_visible:
            self.filtrado_container.visible = False
            self.card_row_container.visible = False
            self.pagination_container.visible = False
            self.digimon_visible = False
        else:
            self.current_page = 1
            self.all_cards = self.digicard_controller.obtener_digicartas()
            self.all_cards.sort(key=lambda x: x.id)
            self.total_pages = (len(self.all_cards) + self.cards_per_page - 1) // self.cards_per_page
            self.mostrar_pagina(self.current_page)
            self.digimon_visible = True
            self.card_row_container.offset = ft.transform.Offset(0, 0)
            self.card_row_container.update()
        self.page.update()

    def cargar_yugioh(self, e):
        # Implementar lógica de carga de cartas de Yugioh
        pass

    def cargar_pokemon(self, e):
        # Implementar lógica de carga de cartas de Pokemon
        pass

    def cargar_magic(self, e):
        # Implementar lógica de carga de cartas de Pokemon
        pass

    def cargar_onepiece(self, e):
        # Implementar lógica de carga de cartas de Pokemon
        pass

    def cargar_lorcana(self, e):
        # Implementar lógica de carga de cartas de Pokemon
        pass

    def mostrar_pagina(self, pagina):
        start_index = (pagina - 1) * self.cards_per_page
        end_index = start_index + self.cards_per_page
        cards_to_show = self.all_cards[start_index:end_index]

        card_row = ft.Row(wrap=True, scroll=ft.ScrollMode.ALWAYS, expand=True)

        for carta in cards_to_show:
            image_proxy_url = carta.image_url
            card_row.controls.append(
                ft.Container(
                    ft.Image(src=image_proxy_url, width=250, height=250),
                    border_radius=ft.border_radius.all(5),
                    padding=ft.padding.all(5),
                    on_click=lambda e, c=carta: self.mostrar_detalle_carta(c)
                )
            )

        self.mostrar_filtro()
        self.card_row_container.content = card_row

        self.card_row_container.visible = True
        self.page.update()
        self.mostrar_paginacion()

    def mostrar_filtro(self):
        filtrado_row = ft.Row(
            controls=[
                ft.Text("Filtro"),
                ft.IconButton(icon=ft.icons.FILTER_LIST)
            ],
            alignment=ft.MainAxisAlignment.END,

        )
        self.filtrado_container.margin = ft.margin.only(right=10)
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

        # Llamar a la función para mostrar el detalle de la carta
        self.details_panel = mostrar_detalle_carta(self.page, carta, self.cerrar_panel_detalles)

    def cerrar_panel_detalles(self, e):
        # Cerrar el panel de detalles si se hace clic fuera del panel
        self.page.overlay.remove(self.details_panel)
        self.details_panel = None
        self.page.update()
