import flet as ft

from views.home_view import HomeView
from views.login_view import LoginView
from views.registro_view import RegistroView
from views.usuario_view import UserView
from views.recargar_view import RecargarView


class Interfaz:
    """
    Clase que maneja la interfaz de usuario utilizando el framework Flet.

    """

    def __init__(self, page: ft.Page):
        """
        Inicializa una nueva instancia de la clase Interfaz.

        Args:
            page (ft.Page): La página principal de la aplicación.
        """
        self.page = page
        self.home_view = HomeView(page)
        self.login_view = LoginView(page)
        self.registro_view = RegistroView(page)
        self.usuario_view = UserView(page)
        self.recargar_view = None

    def iniciar(self) -> None:
        """
        Inicializa el manejo de rutas y establece la ruta inicial.
        """
        self.page.on_route_change = self.route_change
        self.page.go("/")

    def route_change(self, route):
        """
        Maneja el cambio de rutas y muestra la vista correspondiente.

        Args:
            route (str): La ruta actual de la aplicación.
        """
        if self.page.route == "/":
            self.home_view.mostrar()
        elif self.page.route == "/login/":
            self.login_view.mostrar()
        elif self.page.route == "/registro/":
            self.registro_view.mostrar()
        elif self.page.route == "/user/":
            self.usuario_view.mostrar()
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
