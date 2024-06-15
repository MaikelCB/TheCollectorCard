import logging
from datetime import timedelta
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from passlib.hash import bcrypt
from typing import List
from .config import get_db, engine, ACCESS_TOKEN_EXPIRE_MINUTES
from .models import Base, Usuario, UsuarioCarta
from .schemas import UsuarioCreate, UsuarioResponse, UsuarioCartaCreate, Token, DigiCartaResponse
from control.user_control import UsuarioController
from control.digicard_control import DigiCardController
from .auth import create_access_token, verify_password, decode_access_token

logging.basicConfig(level=logging.INFO)

# Crear todas las tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Inicializar la aplicación FastAPI
app = FastAPI()

# Inicializar los controladores
controller = UsuarioController()
digicard_controller = DigiCardController()

# Configurar el esquema OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Obtiene el usuario actual autenticado a partir del token de acceso.

    Args:
        token (str): El token de acceso.
        db (Session): La sesión de la base de datos.

    Returns:
        Usuario: El usuario autenticado.

    Raises:
        HTTPException: Si el token es inválido o si el usuario no existe.
    """
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
    user = db.query(Usuario).filter(Usuario.email == username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


@app.get("/me/", response_model=UsuarioResponse)
def read_users_me(current_user: Usuario = Depends(get_current_user)):
    """
    Endpoint para obtener la información del usuario actual autenticado.

    Args:
        current_user (Usuario): El usuario autenticado.

    Returns:
        Usuario: La información del usuario autenticado.
    """
    return current_user


@app.post("/usuarios/", response_model=UsuarioResponse)
def create_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    """
    Endpoint para crear un nuevo usuario.

    Args:
        usuario (UsuarioCreate): Los datos del usuario a crear.
        db (Session): La sesión de la base de datos.

    Returns:
        Usuario: La información del usuario creado.

    Raises:
        HTTPException: Si las contraseñas no coinciden o si hay un error en el registro.
    """
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
    """
    Endpoint para el inicio de sesión de usuarios.

    Args:
        form_data (OAuth2PasswordRequestForm): Los datos del formulario de inicio de sesión.
        db (Session): La sesión de la base de datos.

    Returns:
        Token: El token de acceso y su tipo.

    Raises:
        HTTPException: Si el nombre de usuario, correo electrónico o la contraseña son inválidos.
    """
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


@app.post("/usuario_cartas/", status_code=201)
def create_or_update_usuario_carta(relacion: UsuarioCartaCreate, db: Session = Depends(get_db)):
    """
    Endpoint para crear o actualizar la relación de cartas de un usuario.

    Args:
        relacion (UsuarioCartaCreate): Los datos de la relación usuario-carta.
        db (Session): La sesión de la base de datos.

    Returns:
        UsuarioCarta: La relación usuario-carta creada o actualizada.
    """
    db_relacion = db.query(UsuarioCarta).filter(
        UsuarioCarta.usuario_id == relacion.usuario_id,
        UsuarioCarta.cardnumber == relacion.cardnumber
    ).first()

    if db_relacion:
        if relacion.cantidad > 0:
            db_relacion.cantidad = relacion.cantidad
            db.commit()
            db.refresh(db_relacion)
        else:
            db.delete(db_relacion)
            db.commit()
    else:
        if relacion.cantidad > 0:
            db_relacion = UsuarioCarta(
                usuario_id=relacion.usuario_id,
                cardnumber=relacion.cardnumber,
                cantidad=relacion.cantidad
            )
            db.add(db_relacion)
            db.commit()
            db.refresh(db_relacion)

    return db_relacion


@app.get("/usuario_cartas/{usuario_id}", response_model=List[UsuarioCartaCreate])
def obtener_usuario_cartas(usuario_id: int, db: Session = Depends(get_db)):
    """
    Endpoint para obtener las cartas de un usuario específico.

    Args:
        usuario_id (int): El identificador del usuario.
        db (Session): La sesión de la base de datos.

    Returns:
        list: Una lista de relaciones usuario-carta.
    """
    usuario_cartas = db.query(UsuarioCarta).filter(UsuarioCarta.usuario_id == usuario_id).all()
    return usuario_cartas


@app.get("/digicartas/", response_model=List[DigiCartaResponse])
def obtener_digicartas(db: Session = Depends(get_db)):
    """
    Endpoint para obtener todas las cartas de Digimon.

    Args:
        db (Session): La sesión de la base de datos.

    Returns:
        list: Una lista de cartas de Digimon.
    """
    return digicard_controller.obtener_digicartas(db)
