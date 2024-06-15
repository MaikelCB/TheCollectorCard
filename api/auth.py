from datetime import datetime, timedelta
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from .models import Usuario
from .schemas import TokenData
from .config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from .bcrypt_wrapper import verify_password, get_password_hash


def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    Crea un token de acceso JWT.

    Args:
        data (dict): Los datos a codificar en el token.
        expires_delta (timedelta, optional): La duración del token. Si no se especifica, el token expira en 15 minutos.

    Returns:
        str: El token de acceso JWT codificado.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str):
    """
    Decodifica un token de acceso JWT.

    Args:
        token (str): El token JWT a decodificar.

    Returns:
        dict: Los datos decodificados del token si es válido, de lo contrario, None.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
