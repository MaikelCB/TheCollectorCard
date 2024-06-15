from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class Usuario(Base):
    """
    Modelo de usuario.

    Atributos:
        id (int): Identificador único del usuario.
        nombre (str): Nombre del usuario.
        email (str): Correo electrónico del usuario.
        password (str): Contraseña del usuario.
        cartas (relationship): Relación con el modelo UsuarioCarta.
    """
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    cartas = relationship("UsuarioCarta", back_populates="owner")


class UsuarioCarta(Base):
    """
    Modelo de relación usuario-carta.

    Atributos:
        id (int): Identificador único de la relación.
        usuario_id (int): Identificador del usuario (clave foránea).
        cardnumber (str): Número de la carta.
        cantidad (int): Cantidad de cartas.
        owner (relationship): Relación con el modelo Usuario.
    """
    __tablename__ = "usuario_cartas"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    cardnumber = Column(String)
    cantidad = Column(Integer, default=0)

    owner = relationship("Usuario", back_populates="cartas")


class DigiCartaBD(Base):
    """
    Modelo de carta de Digimon.

    Atributos:
        id (str): Identificador único de la carta.
        name (str): Nombre de la carta.
        type (str): Tipo de la carta.
        level (str): Nivel de la carta.
        play_cost (str): Costo de juego de la carta.
        evolution_cost (str): Costo de evolución de la carta.
        evolution_color (str): Color de evolución de la carta.
        evolution_level (str): Nivel de evolución de la carta.
        xros_req (str): Requisitos de Xros de la carta.
        color (str): Color principal de la carta.
        color2 (str): Color secundario de la carta (opcional).
        digi_type (str): Tipo de Digimon de la carta.
        digi_type2 (str): Segundo tipo de Digimon de la carta (opcional).
        form (str): Forma de la carta.
        dp (str): Puntos de poder de la carta.
        attribute (str): Atributo de la carta.
        rarity (str): Rareza de la carta.
        stage (str): Etapa de la carta.
        artist (str): Artista de la carta.
        main_effect (str): Efecto principal de la carta.
        source_effect (str): Efecto de la fuente de la carta.
        alt_effect (str): Efecto alternativo de la carta.
        series (str): Serie de la carta.
        image_url (str): URL de la imagen de la carta.
    """
    __tablename__ = "digicartas"

    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    type = Column(String)
    level = Column(String)
    play_cost = Column(String)
    evolution_cost = Column(String)
    evolution_color = Column(String)
    evolution_level = Column(String)
    xros_req = Column(String)
    color = Column(String)
    color2 = Column(String, nullable=True)
    digi_type = Column(String)
    digi_type2 = Column(String, nullable=True)
    form = Column(String)
    dp = Column(String)
    attribute = Column(String)
    rarity = Column(String)
    stage = Column(String)
    artist = Column(String)
    main_effect = Column(String)
    source_effect = Column(String)
    alt_effect = Column(String)
    series = Column(String)
    image_url = Column(String)
