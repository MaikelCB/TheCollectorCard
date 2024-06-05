from email_validator import validate_email, EmailNotValidError
from passlib.hash import bcrypt
import sqlite3


class UsuarioController:

    def registrar_usuario(self, nombre, email, password):
        # Validar email
        try:
            valid = validate_email(email)
            email = valid.normalized
        except EmailNotValidError as e:
            return {"status": "error", "message": "ErrorEmail"}

        # Validar contraseña
        if len(password) < 8:
            return {"status": "error", "message": "ErrorPWD"}

        # Encriptar contraseña
        hashed_password = bcrypt.hash(password)

        # Insertar en la base de datos
        conn = sqlite3.connect('mi_db.sqlite')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios (nombre, email, password) VALUES (?, ?, ?)", (nombre, email, hashed_password))
        conn.commit()
        conn.close()
        return {"status": "success", "message": "Usuario registrado correctamente"}
