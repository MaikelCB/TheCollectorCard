import logging
from datetime import timedelta
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from passlib.hash import bcrypt  # Asegúrate de importar bcrypt aquí
from .config import get_db, engine, ACCESS_TOKEN_EXPIRE_MINUTES
from .models import Base, Usuario, UsuarioCarta
from .schemas import UsuarioCreate, UsuarioResponse, UsuarioCartaCreate, Token
from control.user_control import UsuarioController
from .auth import create_access_token, verify_password, decode_access_token

logging.basicConfig(level=logging.INFO)

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI()
controller = UsuarioController()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    username: str = payload.get("sub")
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return username


@app.post("/usuarios/", response_model=UsuarioResponse)
def create_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    logging.info("Creating user: %s", usuario.email)
    if usuario.password != usuario.confirm_password:
        logging.error("Passwords do not match")
        raise HTTPException(status_code=400, detail="Passwords do not match")

    result = controller.registrar_usuario(db, usuario)

    if result["status"] == "error":
        logging.error("Error creating user: %s", result["detail"])
        raise HTTPException(status_code=400, detail=result["detail"])

    logging.info("User created successfully: %s", usuario.email)
    return db.query(Usuario).filter(Usuario.email == usuario.email).first()


@app.post("/login/", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(
        (Usuario.email == form_data.username) |
        (Usuario.nombre == form_data.username)
    ).first()

    if not user:
        raise HTTPException(status_code=400, detail="Invalid username or email")

    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/usuario_cartas/")
def create_usuario_carta(relacion: UsuarioCartaCreate, db: Session = Depends(get_db)):
    db_relacion = UsuarioCarta(
        usuario_id=relacion.usuario_id,
        cardnumber=relacion.cardnumber,  # Usar cardnumber en lugar de carta_id
        cantidad=relacion.cantidad
    )
    db.add(db_relacion)
    db.commit()
    db.refresh(db_relacion)
    return db_relacion
