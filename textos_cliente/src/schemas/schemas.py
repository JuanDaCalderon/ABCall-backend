from typing import Union
from pydantic import BaseModel

class texto(BaseModel):
    saludo: Union[str,None] = None
    cierre: Union[str,None] = None
    clienteid: Union[str,None] = None

class textoUpdate(BaseModel):
    id: Union[int,None] = None
    saludo: Union[str,None] = None
    cierre: Union[str,None] = None
    clienteid: Union[str,None] = None



