import requests
from models.digicard import DigiCarta
from models.usuario_cartas import UsuarioCarta


class DigiCardController:
    def __init__(self):
        self.api_url = "https://digimoncard.io/api-public/search.php?series=Digimon Card Game"
        self.proxy_url = "http://127.0.0.1:50739/proxy?url="
        self.api_base_url = "http://127.0.0.1:8001"  # Asegúrate de que este puerto sea el correcto

    def obtener_digicartas(self):
        response = requests.get(self.api_url)
        digimons = response.json()
        cartas = []

        for digimon in digimons:
            carta = DigiCarta(
                name=digimon["name"],
                type=digimon["type"],
                color=digimon["color"],
                stage=digimon["stage"],
                digi_type=digimon["digi_type"],
                attribute=digimon.get("attribute"),
                level=digimon["level"],
                play_cost=digimon.get("play_cost"),
                evolution_cost=digimon.get("evolution_cost"),
                cardrarity=digimon["cardrarity"],
                artist=digimon["artist"],
                dp=digimon.get("dp"),
                cardnumber=digimon["cardnumber"],
                maineffect=digimon.get("maineffect"),
                soureeffect=digimon["soureeffect"],
                set_name=digimon["set_name"],
                card_sets=digimon["card_sets"],
                image_url=digimon["image_url"]
            )
            cartas.append(carta)

        return cartas

    def obtener_cantidad_carta(self, usuario_id, cardnumber):
        response = requests.get(f"{self.api_base_url}/usuario_cartas/{usuario_id}/{cardnumber}")
        if response.status_code == 200:
            return response.json().get('cantidad', 0)
        return 0

    def actualizar_cantidad_carta(self, usuario_id, cardnumber, cantidad):
        data = {
            "usuario_id": usuario_id,
            "cardnumber": cardnumber,
            "cantidad": cantidad
        }
        response = requests.post(f"{self.api_base_url}/usuario_cartas/", json=data)
        return response.status_code == 200
