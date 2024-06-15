from email_validator import validate_email, EmailNotValidError
from sqlalchemy.orm import Session
from api.models import Usuario
from api.schemas import UsuarioCreate
from api.bcrypt_wrapper import get_password_hash


class UsuarioController:
    """
    Clase para controlar las operaciones relacionadas con los usuarios.

    Métodos:
        registrar_usuario(db: Session, usuario: UsuarioCreate) -> dict: Registra un nuevo usuario en la base de datos.
    """

    def registrar_usuario(self, db: Session, usuario: UsuarioCreate):
        """
        Registra un nuevo usuario en la base de datos.

        Args:
            db (Session): La sesión de la base de datos.
            usuario (UsuarioCreate): El esquema de datos del usuario a registrar.

        Returns:
            dict: Un diccionario con el estado de la operación y un mensaje detallado.
        """
        try:
            # Validar el correo electrónico
            try:
                valid = validate_email(usuario.email)
                email = valid.email
            except EmailNotValidError:
                return {"status": "error", "detail": "Invalid email"}

            # Validar la longitud de la contraseña
            if len(usuario.password) < 8:
                return {"status": "error", "detail": "Password too short"}

            # Hashear la contraseña
            hashed_password = get_password_hash(usuario.password)

            # Crear una nueva instancia de Usuario
            db_usuario = Usuario(nombre=usuario.nombre, email=email, password=hashed_password)

            # Agregar el nuevo usuario a la base de datos
            db.add(db_usuario)
            db.commit()
            db.refresh(db_usuario)

            return {"status": "success", "message": "Usuario registrado correctamente"}

        except Exception as e:
            return {"status": "error", "detail": str(e)}
