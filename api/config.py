from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# URL de la base de datos
DATABASE_URL = "sqlite:///../db.collector.db"

# Creación del motor de la base de datos
engine = create_engine(DATABASE_URL)

# Configuración de la sesión de la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    Generador de la sesión de la base de datos.

    Yields:
        db: Una sesión de la base de datos.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Configuración de seguridad
SECRET_KEY = os.getenv("SECRET_KEY", "hola1234")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
