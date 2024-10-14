from typing import List, Union
from pydantic import BaseModel

class permiso(BaseModel):
    NOMBRE: Union[str, None] = None
    ESTADO: Union[bool, None] = None

    class Config:
        from_attributes = True

class permisoid(BaseModel):
    ID: int = None
    class Config:
        from_attributes = True
        
class role(BaseModel):
    NOMBRE: Union[str, None] = None
    class Config:
        from_attributes = True
        
class roleSchema(BaseModel):
    ID: int = None
    NOMBRE: str = None
    PERMISOS: List[permisoid] = None
    class Config:
        from_attributes = True
class PermisoUpdate(BaseModel):
    PERMISOS: Union[List[permisoid], None] = None