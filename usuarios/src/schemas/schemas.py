from typing import Union
from pydantic import BaseModel


class TokenStatusCheck(BaseModel):
    token: Union[str, None] = None


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenObject(BaseModel):
    email: Union[str, None] = None
    username: Union[str, None] = None
    exp: Union[int, None] = None

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: Union[str, None] = None
    password: Union[str, None] = None

    class Config:
        from_attributes = True


class UserRegister(BaseModel):
    email: Union[str, None] = None
    username: Union[str, None] = None
    password: Union[str, None] = None
    nombres: Union[str, None] = None
    apellidos: Union[str, None] = None

    class Config:
        from_attributes = True

class ClienteRegister(BaseModel):
    nombre: Union[str, None] = None
    email: Union[str, None] = None
    telefono: Union[str, None] = None
    direccion: Union[str, None] = None
    
    class Config:
        from_attributes = True

class ClienteResponse(BaseModel):
    id: Union[str, None] = None
    nombre: Union[str, None] = None
    email: Union[str, None] = None
    telefono: Union[str, None] = None
    direccion: Union[str, None] = None
    
    class Config:
        from_attributes = True