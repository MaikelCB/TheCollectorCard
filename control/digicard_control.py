import requests
from models.digicard import DigiCarta


class DigiCardController:
    def __init__(self):
        self.api_url = "https://digimoncard.io/api-public/search.php?series=Digimon Card Game"
        self.proxy_url = "http://127.0.0.1:50739/proxy?url="

    def obtener_digicartas(self, set_name_filter):
        response = requests.get(self.api_url)
        digimons = response.json()
        cartas = []

        for digimon in digimons:
            if digimon["set_name"] == set_name_filter:
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
