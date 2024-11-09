from typing import Union
from pydantic import BaseModel


class AsociacionPermisos(BaseModel):
    rol_id: Union[int, None] = None
    permiso_id: Union[int, None] = None

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
    telefono: Union[str, None] = None
    password: Union[str, None] = None
    nombres: Union[str, None] = None
    apellidos: Union[str, None] = None
    direccion: Union[str, None] = None
    gestortier: Union[str, None] = None
    rol: Union[int, None] = None

    class Config:
        from_attributes = True
