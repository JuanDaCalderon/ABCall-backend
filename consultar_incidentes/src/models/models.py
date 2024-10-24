import enum
import uuid
from sqlalchemy import BigInteger, Column, String, DateTime , ForeignKey, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, mapped_column
from ..database import database


class Incidentes(database.Base):
    __tablename__ = "INCIDENTES"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    cliente =  mapped_column(ForeignKey("USUARIOS.id", ondelete="CASCADE"))
    fechacreacion = Column(DateTime)
    usuario =  mapped_column(ForeignKey("USUARIOS.id", ondelete="CASCADE"))
    correo = Column(String)
    direccion = Column(String)
    telefono = Column(String)
    descripcion = Column(String)
    prioridad = Column(String)
    estado = Column(String)
    COMENTARIOS = Column(String)

class GestorTiers(enum.Enum):
    junior = 'junior'
    mid = 'mid'
    senior = 'senior'
    lead = 'lead'
    manager = 'manager'

class Usuarios(database.Base):
    __tablename__ = "USUARIOS"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    telefono = Column(String, unique=True)
    password = Column(String)
    nombres = Column(String)
    apellidos = Column(String)
    direccion = Column(String)
    fechacreacion = Column(DateTime)
    gestortier = Column(Enum(GestorTiers))
    roleid = mapped_column(ForeignKey("ROLES.id", ondelete="CASCADE"))
    roles = relationship("Roles", back_populates="usuario")




database.Base.metadata.create_all(bind=database.engine)
