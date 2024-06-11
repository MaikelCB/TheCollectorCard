from email_validator import validate_email, EmailNotValidError
from sqlalchemy.orm import Session
from api.models import Usuario
from api.schemas import UsuarioCreate
from api.bcrypt_wrapper import verify_password, get_password_hash


class UsuarioController:

    def registrar_usuario(self, db: Session, usuario: UsuarioCreate):
        try:
            # Validar email
            try:
                valid = validate_email(usuario.email)
                email = valid.email
            except EmailNotValidError:
                return {"status": "error", "detail": "Invalid email"}

            # Validar contraseña
            if len(usuario.password) < 8:
                return {"status": "error", "detail": "Password too short"}

            # Encriptar contraseña
            hashed_password = get_password_hash(usuario.password)

            # Insertar en la base de datos
            db_usuario = Usuario(nombre=usuario.nombre, email=email, password=hashed_password)
            db.add(db_usuario)
            db.commit()
            db.refresh(db_usuario)
            return {"status": "success", "message": "Usuario registrado correctamente"}

        except Exception as e:
            return {"status": "error", "detail": str(e)}
