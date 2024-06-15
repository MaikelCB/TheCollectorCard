class DigiCarta:
    def __init__(self, name, type, id, level, play_cost, evolution_cost, evolution_color,
                 evolution_level, xros_req, color, color2, digi_type, digi_type2, form,
                 dp, attribute, rarity, stage, artist, main_effect, source_effect,
                 alt_effect, series, image_url=None):
        """
        Inicializa una nueva instancia de la clase DigiCarta.
        """
        self.name = name
        self.type = type
        self.id = id
        self.level = level
        self.play_cost = play_cost
        self.evolution_cost = evolution_cost
        self.evolution_color = evolution_color
        self.evolution_level = evolution_level
        self.xros_req = xros_req
        self.color = color
        self.color2 = color2
        self.digi_type = digi_type
        self.digi_type2 = digi_type2
        self.form = form
        self.dp = dp
        self.attribute = attribute
        self.rarity = rarity
        self.stage = stage
        self.artist = artist
        self.main_effect = main_effect
        self.source_effect = source_effect
        self.alt_effect = alt_effect
        self.series = series
        self.image_url = image_url
