import flet as ft
from views.interfaz import Interfaz
import subprocess
import sys


def main(page: ft.Page):
    """
    Función principal que inicializa la aplicación Flet.

    Args:
        page (ft.Page): La página principal de la aplicación Flet.

    Comentarios:
        La línea comentada `proxy_process` se utiliza para iniciar un proceso de proxy ejecutando un archivo Python `proxy.py`.
        ERROR en el subprocess del proxy, se comenta esta línea.
    """
    # proxy_process = subprocess.Popen([sys.executable, 'proxy.py'])

    app = Interfaz(page)  # Instancia de la clase Interfaz
    app.iniciar()  # Llamada al método iniciar de la clase Interfaz para iniciar la aplicación


if __name__ == "__main__":
    """
    Punto de entrada de la aplicación. 
    Inicia la aplicación Flet con la función `main` como objetivo, utilizando la carpeta `assets` para los recursos
    y abriendo la aplicación en el navegador web.
    """
    ft.app(target=main, assets_dir='assets', view=ft.WEB_BROWSER)
