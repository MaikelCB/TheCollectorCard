from flask import Flask, request, Response
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Habilitar CORS en toda la aplicación


@app.route('/proxy')
def proxy():
    image_url = request.args.get('url')
    response = requests.get(image_url)
    return Response(response.content, status=response.status_code, content_type=response.headers['Content-Type'])


if __name__ == '__main__':
    app.run(port=50739)
