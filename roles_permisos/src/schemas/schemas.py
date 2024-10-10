from typing import List, Union
from pydantic import BaseModel

class permiso(BaseModel):
    nombre: Union[str, None] = None
    estado: Union[bool, None] = None

    class Config:
        from_attributes = True

class role(BaseModel):
    nombre: Union[str, None] = None
    permisos: Union[List[permiso], None] = None
    class Config:
        from_attributes = True
        
class PermisoUpdate(BaseModel):
    permisos: List[permiso]