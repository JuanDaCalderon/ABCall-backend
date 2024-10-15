from sqlalchemy import Column, String
import uuid
from sqlalchemy.dialects.postgresql import UUID
from ..database import database


class Usuarios(database.Base):
    __tablename__ = "USUARIOS"
    ID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    EMAIL = Column(String, unique=True)
    USERNAME = Column(String, unique=True)
    PASSWORD = Column(String)
    NOMBRES = Column(String)
    APELLIDOS = Column(String)

class Cliente(database.Base):
    __tablename__ = "CLIENTE"
    ID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    NOMBRE = Column(String)
    EMAIL = Column(String, unique=True)
    TELEFONO = Column(String)
    DIRECCION = Column(String)
    
    
database.Base.metadata.create_all(bind=database.engine)
