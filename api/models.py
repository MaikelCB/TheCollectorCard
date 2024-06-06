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
    carta_id = Column(Integer)
    cantidad = Column(Integer, default=0)

    owner = relationship("Usuario", back_populates="cartas")
