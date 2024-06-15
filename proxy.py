from flask import Flask, request, Response
import requests
from flask_cors import CORS

# Inicialización de la aplicación Flask
app = Flask(__name__)
CORS(app)  # Habilitación de CORS para permitir solicitudes desde diferentes orígenes


@app.route('/proxy')
def proxy():
    """
    Endpoint del proxy para redirigir solicitudes de imágenes.

    Args:
        No se requieren argumentos directos, pero espera un parámetro de consulta 'url' en la solicitud.

    Returns:
        Response: La respuesta contiene el contenido de la imagen solicitada, el código de estado y el tipo de contenido.
    """
    image_url = request.args.get('url')  # Obtención de la URL de la imagen desde los parámetros de la consulta
    response = requests.get(image_url)  # Realización de la solicitud GET a la URL de la imagen
    return Response(response.content, status=response.status_code, content_type=response.headers['Content-Type'])
    # Devolución de la respuesta con el contenido de la imagen, el estado y el tipo de contenido

if __name__ == '__main__':
    """
    Punto de entrada de la aplicación Flask. 
    Inicia el servidor en el puerto 50739.
    """
    app.run(port=50739)
