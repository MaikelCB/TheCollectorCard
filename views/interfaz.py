import flet as ft
from views.home_view import HomeView
from views.login_view import LoginView
from views.registro_view import RegistroView
from views.recargar_view import RecargarView  # Importar la vista de recarga

class Interfaz:
    def __init__(self, page: ft.Page):
        self.page = page
        self.home_view = HomeView(page)
        self.login_view = LoginView(page)
        self.registro_view = RegistroView(page)
        self.recargar_view = None  # Vista de recarga se crea dinámicamente

    def iniciar(self) -> None:
        self.page.on_route_change = self.route_change
        self.page.go("/")

    def route_change(self, route):
        if self.page.route == "/":
            self.home_view.mostrar()
        elif self.page.route == "/login/":
            self.login_view.mostrar()
        elif self.page.route == "/registro/":
            self.registro_view.mostrar()
        elif self.page.route.startswith("/recargar"):
            target = self.page.route.split("?target=")[-1]
            self.recargar_view = RecargarView(self.page, target)
            self.recargar_view.mostrar()
        else:
            self.page.views.clear()
            self.page.views.append(ft.View(
                "/404",
                controls=[ft.Text("Página no encontrada")],
            ))
            self.page.update()
