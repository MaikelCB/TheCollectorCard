from pydantic import BaseModel, EmailStr, constr


class UsuarioCreate(BaseModel):
    nombre: str
    email: EmailStr
    password: constr(min_length=8)
    confirm_password: str


class UsuarioResponse(BaseModel):
    id: int
    nombre: str
    email: str

    class Config:
        from_attributes = True  # Actualizado para Pydantic v2


class UsuarioCartaCreate(BaseModel):
    usuario_id: int
    cardnumber: str  # Usar cardnumber en lugar de carta_id
    cantidad: int


class LoginRequest(BaseModel):
    username_or_email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
