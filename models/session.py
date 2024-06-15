class Session:
    """
    Clase para manejar el estado de la sesión del usuario.

    Atributos de Clase:
        logged_in (bool): Indica si el usuario ha iniciado sesión.
        user_name (str): Nombre del usuario.
        user_id (int or None): Identificador del usuario.

    Métodos de Clase:
        login(cls, user_id, user_name): Inicia la sesión del usuario con el ID y el nombre proporcionados.
        logout(cls): Cierra la sesión del usuario.
    """

    logged_in = False
    user_name = ""
    user_id = None

    @classmethod
    def login(cls, user_id, user_name):
        """
        Inicia la sesión del usuario.

        Args:
            user_id (int): El identificador del usuario.
            user_name (str): El nombre del usuario.
        """
        cls.logged_in = True
        cls.user_id = user_id
        cls.user_name = user_name

    @classmethod
    def logout(cls):
        """
        Cierra la sesión del usuario.
        """
        cls.logged_in = False
        cls.user_id = None
        cls.user_name = ""
