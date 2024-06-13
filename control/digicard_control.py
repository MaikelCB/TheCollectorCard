import requests
from models.digicard import DigiCarta
from models.usuario_cartas import UsuarioCarta


class DigiCardController:
    def __init__(self):
        self.api_url = "https://digimoncard.io/api-public/search.php?series=Digimon Card Game"
        self.proxy_url = "http://127.0.0.1:50739/proxy?url="
        self.api_base_url = "http://127.0.0.1:8001"
        self.bannerdigimon_image_url = "https://millenniumgames.com/wp-content/uploads/2021/02/digimon-card-game-banner-e1613093475652.jpg"
        self.bannerpokemon_image_url = "https://www.boardsandswords.co.uk/cdn/shop/files/poke-hero_bac2afe6-8cfd-4937-bd90-f1069ce4e256_1800x.png"
        self.banneryugioh_image_url = "https://egdgames.com/storage/2024/06/banner-yugioh-tcg.webp"
        self.bannermagic_image_url = "https://static.posters.cz/image/hp/77610.jpg"
        self.banneronepiece_image_url = "https://www.gametrade.it/images/testate/onepiece_testata_gametrade.jpg"
        self.bannerlorcana_image_url = "https://www.waylandgames.co.uk/media/wysiwyg/Disney_Lorcana_Banner_1.jpg"
        self.fondo_image_url = "https://www.teahub.io/photos/full/284-2849092_fondos-de-color-gris-oscuro.jpg"


    def obtener_digicartas(self):
        response = requests.get(self.api_url)
        digimons = response.json()
        cartas = []

        for digimon in digimons:
            if digimon["series"] == "Digimon Card Game":
                carta = DigiCarta(
                    name=digimon.get("name", "Unknown"),
                    type=digimon.get("type", "Unknown"),
                    id=digimon.get("id", "Unknown"),
                    level=digimon.get("level", "Unknown"),
                    play_cost=digimon.get("play_cost", "Unknown"),
                    evolution_cost=digimon.get("evolution_cost", "Unknown"),
                    evolution_color=digimon.get("evolution_color", "Unknown"),
                    evolution_level=digimon.get("evolution_level", "Unknown"),
                    xros_req=digimon.get("xros_req", "Unknown"),
                    color=digimon.get("color", "Unknown"),
                    color2=digimon.get("color2", None),
                    digi_type=digimon.get("digi_type", "Unknown"),
                    digi_type2=digimon.get("digi_type2", None),
                    form=digimon.get("form", "Unknown"),
                    dp=digimon.get("dp", "Unknown"),
                    attribute=digimon.get("attribute", "Unknown"),
                    rarity=digimon.get("rarity", "Unknown"),
                    stage=digimon.get("stage", "Unknown"),
                    artist=digimon.get("artist", "Unknown"),
                    main_effect=digimon.get("main_effect", "Unknown"),
                    source_effect=digimon.get("source_effect", "Unknown"),
                    alt_effect=digimon.get("alt_effect", "Unknown"),
                    series=digimon.get("series", "Unknown")
                )
                carta.image_url = self.obtener_imagen_carta(carta.id)
                cartas.append(carta)

        return cartas

    def obtener_imagen_carta(self, cardnumber):
        image_url = f"https://images.digimoncard.io/images/cards/{cardnumber}.jpg"
        return f"{self.proxy_url}{image_url}"

    def obtener_cartas_usuario(self, usuario_id):
        response = requests.get(f"{self.api_base_url}/usuario_cartas/{usuario_id}")
        if response.status_code == 200:
            return {carta["cardnumber"]: carta["cantidad"] for carta in response.json()}
        return {}

    def obtener_cantidad_carta(self, usuario_id, cardnumber):
        response = requests.get(f"{self.api_base_url}/usuario_cartas/{usuario_id}/{cardnumber}")
        if response.status_code == 200:
            return response.json()["cantidad"]
        return 0

    def actualizar_cantidad_carta(self, usuario_id, cardnumber, cantidad):
        response = requests.post(f"{self.api_base_url}/usuario_cartas/", json={
            "usuario_id": usuario_id,
            "cardnumber": cardnumber,
            "cantidad": cantidad
        })
        return response.status_code == 201

    def obtener_fondo_image(self):
        return f"{self.proxy_url}{self.fondo_image_url}"

    def obtener_bannerdigimon_image(self):
        return f"{self.proxy_url}{self.bannerdigimon_image_url}"

    def obtener_bannerpokemon_image(self):
        return f"{self.proxy_url}{self.bannerpokemon_image_url}"

    def obtener_banneryugioh_image(self):
        return f"{self.proxy_url}{self.banneryugioh_image_url}"

    def obtener_bannermagic_image(self):
        return f"{self.proxy_url}{self.bannermagic_image_url}"

    def obtener_banneronepiece_image(self):
        return f"{self.proxy_url}{self.banneronepiece_image_url}"

    def obtener_bannerlorcana_image(self):
        return f"{self.proxy_url}{self.bannerlorcana_image_url}"
