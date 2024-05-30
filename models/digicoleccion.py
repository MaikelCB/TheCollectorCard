class DigiColeccion:
    def __init__(self, set_name):
        self.set_name = set_name
        self.cartas = []

    def agregar_carta(self, carta):
        self.cartas.append(carta)
