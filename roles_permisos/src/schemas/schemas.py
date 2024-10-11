from typing import List, Union
from pydantic import BaseModel

class permiso(BaseModel):
    nombre: Union[str, None] = None
    estado: Union[bool, None] = None

    class Config:
        from_attributes = True

class permisoid(BaseModel):
    id: int = None
    class Config:
        from_attributes = True
        
class role(BaseModel):
    nombre: Union[str, None] = None
    class Config:
        from_attributes = True
        
class roleSchema(BaseModel):
    id: int = None
    nombre: str = None
    permisos: List[permisoid] = None
    class Config:
        from_attributes = True
class PermisoUpdate(BaseModel):
    permisos: Union[List[permisoid], None] = None