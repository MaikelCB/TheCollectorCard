from pydantic import BaseModel, EmailStr, constr


class UsuarioCreate(BaseModel):
    """
    Esquema de Pydantic para la creación de un usuario.

    Atributos:
        nombre (str): Nombre del usuario.
        email (EmailStr): Correo electrónico del usuario.
        password (constr): Contraseña del usuario con una longitud mínima de 8 caracteres.
        confirm_password (str): Confirmación de la contraseña del usuario.
    """
    nombre: str
    email: EmailStr
    password: constr(min_length=8)
    confirm_password: str


class UsuarioResponse(BaseModel):
    """
    Esquema de Pydantic para la respuesta de información de un usuario.

    Atributos:
        id (int): Identificador único del usuario.
        nombre (str): Nombre del usuario.
        email (str): Correo electrónico del usuario.
    """
    id: int
    nombre: str
    email: str

    class Config:
        from_attributes = True


class UsuarioCartaCreate(BaseModel):
    """
    Esquema de Pydantic para la creación o actualización de la relación usuario-carta.

    Atributos:
        usuario_id (int): Identificador del usuario.
        cardnumber (str): Número de la carta.
        cantidad (int): Cantidad de cartas.
    """
    usuario_id: int
    cardnumber: str
    cantidad: int


class LoginRequest(BaseModel):
    """
    Esquema de Pydantic para la solicitud de inicio de sesión.

    Atributos:
        username_or_email (str): Nombre de usuario o correo electrónico.
        password (str): Contraseña del usuario.
    """
    username_or_email: str
    password: str


class Token(BaseModel):
    """
    Esquema de Pydantic para la respuesta del token de acceso.

    Atributos:
        access_token (str): Token de acceso.
        token_type (str): Tipo de token.
    """
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    Esquema de Pydantic para los datos del token.

    Atributos:
        username (str | None): Nombre de usuario, opcional.
    """
    username: str | None = None


class DigiCartaResponse(BaseModel):
    """
    Esquema de Pydantic para la respuesta de información de una carta de Digimon.

    Atributos:
        id (str): Identificador único de la carta.
        name (str): Nombre de la carta.
        type (str): Tipo de la carta.
        level (str): Nivel de la carta.
        play_cost (str): Costo de juego de la carta.
        evolution_cost (str): Costo de evolución de la carta.
        evolution_color (str): Color de evolución de la carta.
        evolution_level (str): Nivel de evolución de la carta.
        xros_req (str): Requisitos de Xros de la carta.
        color (str): Color principal de la carta.
        color2 (str | None): Color secundario de la carta, opcional.
        digi_type (str): Tipo de Digimon de la carta.
        digi_type2 (str | None): Segundo tipo de Digimon de la carta, opcional.
        form (str): Forma de la carta.
        dp (str): Puntos de poder de la carta.
        attribute (str): Atributo de la carta.
        rarity (str): Rareza de la carta.
        stage (str): Etapa de la carta.
        artist (str): Artista de la carta.
        main_effect (str): Efecto principal de la carta.
        source_effect (str): Efecto de la fuente de la carta.
        alt_effect (str): Efecto alternativo de la carta.
        series (str): Serie de la carta.
        image_url (str): URL de la imagen de la carta.
    """
    id: str
    name: str
    type: str
    level: str
    play_cost: str
    evolution_cost: str
    evolution_color: str
    evolution_level: str
    xros_req: str
    color: str
    color2: str | None = None
    digi_type: str
    digi_type2: str | None = None
    form: str
    dp: str
    attribute: str
    rarity: str
    stage: str
    artist: str
    main_effect: str
    source_effect: str
    alt_effect: str
    series: str
    image_url: str

    class Config:
        from_attributes = True
