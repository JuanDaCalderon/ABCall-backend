from typing import Union
from pydantic import BaseModel


class Incidentes(BaseModel):
    descripcion: Union[str, None] = None
    estado: Union[str, None] = None
    fechacreacion: Union[str, None] = None
    gestorabc: Union[str, None] = None
    cliente: Union[str, None] = None
    usuario: Union[str, None] = None
    comentarios: Union[str, None] = None

    class Config:
        from_attributes = True
