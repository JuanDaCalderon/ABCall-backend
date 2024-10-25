from typing import Union
from pydantic import BaseModel


class Incidentes(BaseModel):
    cliente: Union[str, None] = None
    fechacreacion: Union[str, None] = None
    usuario: Union[str, None] = None
    correo: Union[str, None] = None
    direccion: Union[str, None] = None
    telefono: Union[str, None] = None
    descripcion: Union[str, None] = None
    prioridad: Union[str, None] = None
    estado: Union[str, None] = None
    comentarios: Union[str, None] = None

    class Config:
        from_attributes = True


class IncidenteEmail(BaseModel):
    correo: Union[str, None] = None
    direccion: Union[str, None] = None
    telefono: Union[str, None] = None
    descripcion: Union[str, None] = None
    prioridad: Union[str, None] = None
    estado: Union[str, None] = None
    comentarios: Union[str, None] = None

    class Config:
        from_attributes = True
