from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from datetime import timedelta

DATABASE_URL = "sqlite:///../db.collector.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Configuraciones JWT
SECRET_KEY = os.getenv("SECRET_KEY", "hola1234")  # Asegúrate de usar una clave secreta segura en producción
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Expiración del token en minutos
