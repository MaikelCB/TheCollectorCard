from models.user import Usuario
import requests
import sqlite3


class UsuarioController:

    def registrar_usuario(self, nombre, email, password):
        conn = sqlite3.connect('mi_db.sqlite')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios (nombre, email, password) VALUES (?, ?, ?)", (nombre, email, password))
        conn.commit()
        conn.close()
        pass

