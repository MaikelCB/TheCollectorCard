import flet as ft


class RecargarView:
    def __init__(self, page: ft.Page, target: str):
        self.page = page
        self.target = target

    def mostrar(self):
        self.page.go(self.target)
        self.page.update()
