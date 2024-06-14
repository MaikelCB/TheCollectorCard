from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    cartas = relationship("UsuarioCarta", back_populates="owner")


class UsuarioCarta(Base):
    __tablename__ = "usuario_cartas"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    cardnumber = Column(String)  # Usar cardnumber como identificador de carta
    cantidad = Column(Integer, default=0)

    owner = relationship("Usuario", back_populates="cartas")


class DigiCartaBD(Base):
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
