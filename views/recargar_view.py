import flet as ft

class RecargarView:
    """
    Clase que maneja la vista de recarga en la aplicación utilizando el framework Flet.

    """

    def __init__(self, page: ft.Page, target: str):
        """
        Inicializa una nueva instancia de la clase RecargarView.

        Args:
            page (ft.Page): La página principal de la aplicación.
            target (str): La ruta a la que se redirigirá después de la recarga.
        """
        self.page = page
        self.target = target

    def mostrar(self):
        """
        Navega a la ruta de destino y actualiza la página.
        """
        self.page.go(self.target)
        self.page.update()
