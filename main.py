import flet as ft
from views.interfaz import Interfaz
import subprocess
import sys


def main(page: ft.Page):
    # Iniciar el proxy en un subproceso
    # proxy_process = subprocess.Popen([sys.executable, 'proxy.py'])

    # Iniciar la aplicación Flet
    app = Interfaz(page)
    app.iniciar()


if __name__ == "__main__":
    ft.app(target=main)
