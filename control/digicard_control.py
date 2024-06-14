import os
import sqlite3
from sqlalchemy.orm import Session
import requests
from api.models import DigiCartaBD
from api.config import SessionLocal
from models.digicard import DigiCarta
from models.usuario_cartas import UsuarioCarta


class DigiCardController:
    def __init__(self):
        self.api_url = "https://digimoncard.io/api-public/search.php?series=Digimon Card Game"
        self.proxy_url = "http://127.0.0.1:50739/proxy?url="
        self.api_base_url = "http://127.0.0.1:8001"

        self.db_path = '../db.collector.db'
        self.img_path = '../img/digicards'

        self.bannerdigimon_image_url = "https://millenniumgames.com/wp-content/uploads/2021/02/digimon-card-game-banner-e1613093475652.jpg"
        self.bannerpokemon_image_url = "https://www.boardsandswords.co.uk/cdn/shop/files/poke-hero_bac2afe6-8cfd-4937-bd90-f1069ce4e256_1800x.png"
        self.banneryugioh_image_url = "https://egdgames.com/storage/2024/06/banner-yugioh-tcg.webp"
        self.bannermagic_image_url = "https://static.posters.cz/image/hp/77610.jpg"
        self.banneronepiece_image_url = "https://www.gametrade.it/images/testate/onepiece_testata_gametrade.jpg"
        self.bannerlorcana_image_url = "https://www.waylandgames.co.uk/media/wysiwyg/Disney_Lorcana_Banner_1.jpg"
        self.fondo_image_url = "https://www.teahub.io/photos/full/284-2849092_fondos-de-color-gris-oscuro.jpg"

    def obtener_digicartas(self):
        db = SessionLocal()
        try:
            digicartas_db = db.query(DigiCartaBD).all()
            digicartas = [
                DigiCarta(
                    name=carta.name,
                    type=carta.type,
                    id=carta.id,
                    level=carta.level,
                    play_cost=carta.play_cost,
                    evolution_cost=carta.evolution_cost,
                    evolution_color=carta.evolution_color,
                    evolution_level=carta.evolution_level,
                    xros_req=carta.xros_req,
                    color=carta.color,
                    color2=carta.color2,
                    digi_type=carta.digi_type,
                    digi_type2=carta.digi_type2,
                    form=carta.form,
                    dp=carta.dp,
                    attribute=carta.attribute,
                    rarity=carta.rarity,
                    stage=carta.stage,
                    artist=carta.artist,
                    main_effect=carta.main_effect,
                    source_effect=carta.source_effect,
                    alt_effect=carta.alt_effect,
                    series=carta.series,
                    image_url=carta.image_url,
                ) for carta in digicartas_db
            ]
            return digicartas
        finally:
            db.close()

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

    def guardar_carta_db(self, carta):
        conexion = sqlite3.connect(self.db_path)
        cursor = conexion.cursor()

        cursor.execute('''
            INSERT OR REPLACE INTO digicartas (
                id, name, type, level, play_cost, evolution_cost, evolution_color,
                evolution_level, xros_req, color, color2, digi_type, digi_type2, form,
                dp, attribute, rarity, stage, artist, main_effect, source_effect, alt_effect,
                series, image_url
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            carta.id, carta.name, carta.type, carta.level, carta.play_cost,
            carta.evolution_cost, carta.evolution_color, carta.evolution_level,
            carta.xros_req, carta.color, carta.color2, carta.digi_type, carta.digi_type2,
            carta.form, carta.dp, carta.attribute, carta.rarity, carta.stage, carta.artist,
            carta.main_effect, carta.source_effect, carta.alt_effect, carta.series,
            carta.image_url
        ))

        conexion.commit()
        conexion.close()

    def descargar_imagen(self, url, cardnumber):
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            ruta_imagen = os.path.join(self.img_path, f"{cardnumber}.jpg")
            with open(ruta_imagen, 'wb') as out_file:
                for chunk in response.iter_content(chunk_size=8192):
                    out_file.write(chunk)
        else:
            print(f"Error al descargar la imagen {cardnumber}: {response.status_code}")
